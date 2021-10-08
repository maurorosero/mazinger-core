#!/usr/bin/python
# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from ansible.plugins.test.core import version_compare
from ansible.utils.display import Display
from uuid import uuid4


class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    _display = Display()

    def _get_task_var(self, name, default=None):
        """Get templated task variable"""

        if name in self.__task_vars:
            ret = self._templar.template(self.__task_vars.get(name))
        else:
            ret = default

        return ret

    def _action(self, action="tower_api_rest", args={}):
        """Return a new ansible action"""

        task = self._task.copy()

        task.args = dict()
        for key in args.keys():
            task.args[key] = args[key]

        action = self._shared_loader_obj.action_loader.get(
            action,
            task=task,
            connection=self._connection,
            play_context=self._play_context,
            loader=self._loader,
            templar=self._templar,
            shared_loader_obj=self._shared_loader_obj
        )

        return action

    def _get_fact(self, name, default=None):
        """Get a fact"""
        result = self.__ansible_facts.get(name,
                                          self.__ansible_facts.get(default))
        return result

    def _gather_role_vars(self):
        """Gather role vars"""

        self.__distributions = \
            self._get_task_var("check_platform_distributions", {})

        self.__variables = \
            self._get_task_var("check_platform_variables", [])

        self.__platform_aliases = \
            self._get_task_var("check_platform_aliases", [])

    def _gather_facts(self):
        """Gather facts"""
        self.__ansible_facts = self._get_task_var("ansible_facts", {})
        self.__ansible_facts_gathered = False
        if "python_version" not in self.__ansible_facts.keys():
            result = self._execute_module(module_name="setup",
                                          module_args=dict(),
                                          task_vars=self.__task_vars)
            if "failed" not in result.keys():
                self.__ansible_facts = result["ansible_facts"]
                self.__ansible_facts_gathered = True
            else:
                raise AnsibleError("Unable to gather facts: {m}"
                                   .format(m=result["module_stderr"]))

    def _gather_distribution_info(self):
        """Gather distribution info"""
        self.__distribution = \
            self._get_fact("ansible_distribution", "distribution").lower()
        self.__distribution_version = \
            str(self._get_fact("ansible_distribution_version",
                               "distribution_version")).lower()
        self.__distribution_alias = \
            self.__platform_aliases.get(self.__distribution,
                                        self.__distribution)
        self.__distributions_names = \
            list(d.lower() for d in self.__distributions.keys())

    def _check_distribution(self):
        """Check distribution"""
        if self.__distribution not in self.__distributions_names \
           and self.__distribution_alias not in self.__distributions_names:
            raise AnsibleError(
                    "{d} distribution is not supported".format(
                                                        d=self.__distribution))

        required_version = \
            self.__distributions.get(self.__distribution, None)
        alias_required_version = \
            self.__distributions.get(self.__distribution_alias, None)

        version_supported = False

        if required_version is not None \
           and version_compare(self.__distribution_version,
                               required_version,
                               ">="):
            version_supported = True

        if alias_required_version is not None \
           and version_compare(self.__distribution_version,
                               alias_required_version,
                               ">="):
            version_supported = True

        if not version_supported:
            raise AnsibleError("{d} distribution version {v} is not supported"
                               .format(d=self.__distribution,
                                       v=self.__distribution_version))

    def _check_variables(self):
        """Check variables"""

        uuid = uuid4()
        for v in self.__variables:
            value = self._get_task_var(v, uuid)
            if value == uuid:
                raise AnsibleError("Required variable {v} is missing"
                                   .format(v=v))

    def run(self, tmp=None, task_vars=None):
        """Run the action module"""
        super(ActionModule, self).run(tmp, task_vars)

        self.__tmp = tmp
        self.__task_vars = task_vars

        try:
            self._gather_role_vars()
            self._gather_facts()
            self._gather_distribution_info()

            if len(self.__distributions.keys()) > 0:
                self._check_distribution()

            if len(self.__variables) > 0:
                self._check_variables()

            ansible_facts = dict()
            if self.__ansible_facts_gathered:
                ansible_facts = self.__ansible_facts
        finally:
            self._remove_tmp_path(self._connection._shell.tmpdir)

        return dict(changed=False, ansible_facts=ansible_facts)
