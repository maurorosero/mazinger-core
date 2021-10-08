# Ansible check_platform role

This is an [Ansible](http://www.ansible.com) role that check minimum platform requirements.

## Role Variables

A list of all the default variables for this role is available in `defaults/main.yml`.

## Dependencies

None.

## Example Playbook

This is an example playbook:

```yaml
---

- hosts: all
  roles:
    - role: amtega.check_platform
      check_platform_distributions:
        centos: 6
        redhat: 7
        fedora: 27
      check_platform_variables:
        - myvar1
        - myvar2
```

## Testing

Tests are based on [molecule with docker containers](https://molecule.readthedocs.io/en/latest/installation.html).

```shell
cd amtega.check_platform

molecule test
```

## License

Copyright (C) 2020 AMTEGA - Xunta de Galicia

This role is free software: you can redistribute it and/or modify it under the terms of:

GNU General Public License version 3, or (at your option) any later version; or the European Union Public License, either Version 1.2 or – as soon they will be approved by the European Commission ­subsequent versions of the EUPL.

This role is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details or European Union Public License for more details.

## Author Information

- Juan Antonio Valiño García.
