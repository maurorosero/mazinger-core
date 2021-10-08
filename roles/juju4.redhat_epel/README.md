[![Build Status - Master](https://travis-ci.org/juju4/ansible-redhat-epel.svg?branch=master)](https://travis-ci.org/juju4/ansible-redhat-epel)
[![Build Status - Devel](https://travis-ci.org/juju4/ansible-redhat-epel.svg?branch=devel)](https://travis-ci.org/juju4/ansible-redhat-epel/branches)
# RedHat EPEL ansible role

A simple ansible role to setup Redhat EPEL
http://fedoraproject.org/wiki/EPEL

## Requirements & Dependencies

### Ansible
It was tested on the following versions:
 * 1.9
 * 2.0
 * 2.2

### Operating systems

Tested with Centos 6 and 7

## Example Playbook

Just include this role in your list.
For example

```
- host: all
  roles:
    - juju4.redhat-epel
```

## Variables

Nothing specific for now.

## Continuous integration

This role has a travis basic test (for github), more advanced with kitchen and also a Vagrantfile (test/vagrant).
Default kitchen config (.kitchen.yml) is lxd-based, while (.kitchen.vagrant.yml) is vagrant/virtualbox based.

Once you ensured all necessary roles are present, You can test with:
```
$ cd /path/to/roles/juju4.redhat-epel
$ kitchen verify
$ kitchen login
$ KITCHEN_YAML=".kitchen.vagrant.yml" kitchen verify
```
or
```
$ cd /path/to/roles/juju4.redhat-epel/test/vagrant
$ vagrant up
$ vagrant ssh
```

## Troubleshooting & Known issues


## License

BSD 2-clause

