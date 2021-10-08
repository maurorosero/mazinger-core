# Ansible proxy_client role

This is an [Ansible](http://www.ansible.com) role which configures proxy client environment variables.

## Variables

A list of all the default variables for this role is available in `defaults/main.yml`.

The role setups the following facts:

- `proxy_client_environment`: contains a dictionary that you can pass directly to the `environment` keyword.

## Usage

This is an example playbook:

```yaml
---

- hosts: all
  roles:
    - role: amtega.proxy_client
      proxy_client_http_proxy: http://acme.local
      proxy_client_https_proxy: https://acme.local
      proxy_client_no_proxy:
        - https://acme2.local
      proxy_client_permanent: no

  tasks:
    - name: A task that needs internet access
      shell: /bin/true
      environment: "{{ proxy_client_environment }}"
```

## Testing

Tests are based on [molecule with docker containers](https://molecule.readthedocs.io/en/latest/installation.html).

```shell
cd amtega.proxy_client

molecule test --all
```

## License

Copyright (C) 2021 AMTEGA - Xunta de Galicia

This role is free software: you can redistribute it and/or modify it under the terms of:

GNU General Public License version 3, or (at your option) any later version; or the European Union Public License, either Version 1.2 or – as soon they will be approved by the European Commission ­subsequent versions of the EUPL.

This role is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details or European Union Public License for more details.

## Author Information

- Juan Antonio Valiño García.
