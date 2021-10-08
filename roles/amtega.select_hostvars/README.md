# Ansible select_hostvars role

This is an [Ansible](http://www.ansible.com) role that setup a fact with a list/dict of hostvars variables that match a name pattern and contains a set of defined attributes.

## Role Variables

A list of all the default variables for this role is available in `defaults/main.yml`.

The role setups the a fact with the name specified in the variable `select_hostvars_query.fact_name` with the list/dict of hostvars that match the criteria.

## Example Playbook

This is an example playbook:

```yaml
---

- hosts: all
  roles:
    - role: amtega.select_hostvars
      vars:
        select_hostvars_query:
          pattern: "ansible_devices"
          attributes:
            - dm-0
        fact_name: devices_facts
```
with this inventory:

```yaml
---
all:
  hosts:
    localhost:
      ansible_connection: local
      ansible_devices_example:
        aaa: 1
      ansible_devices_test:
        bbb: 2

```
will generate this fact:

```yaml
---
devices_facts:
  aaa: 1
  bbb: 2
```

## Testing

Tests are based on [molecule with docker containers](https://molecule.readthedocs.io/en/latest/installation.html).

```shell
cd amtega.select_hostvars

molecule test --all
```

## License

Copyright (C) 2021 AMTEGA - Xunta de Galicia

This role is free software: you can redistribute it and/or modify it under the terms of:

GNU General Public License version 3, or (at your option) any later version; or the European Union Public License, either Version 1.2 or – as soon they will be approved by the European Commission ­subsequent versions of the EUPL.

This role is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details or European Union Public License for more details.

## Author Information

- Juan Antonio Valiño García.
