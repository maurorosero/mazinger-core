# Amtega gitlab_cli role

This is an [Ansible](http://www.ansible.com) role to setup GitLab command line client.

## Role Variables

A list of all the default variables for this role is available in `defaults/main.yml`. Therole setup the following facts:

- `gitlab_cli_path`: path to the GitLab command line client

## Example Playbook

This is an example playbook:

``` yaml
---
- hosts: localhost
  roles:  
    - amtega.gitlab_cli
  vars:    
    gitlab_cli_server_url: https://www.github.com
    gitlab_cli_login_token: agitlabtokenramdloygenerated
    gitlab_cli_api_version: 4
```

## Testing

Tests are based on [molecule with docker containers](https://molecule.readthedocs.io/en/latest/installation.html).

```shell
cd amtega.gitlab_cli

molecule test
```

## License

Copyright (C) 2020 AMTEGA - Xunta de Galicia

This role is free software: you can redistribute it and/or modify it under the terms of:

GNU General Public License version 3, or (at your option) any later version; or the European Union Public License, either Version 1.2 or – as soon they will be approved by the European Commission ­subsequent versions of the EUPL.

This role is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details or European Union Public License for more details.

## Author Information

- Juan Antonio Valiño García.
