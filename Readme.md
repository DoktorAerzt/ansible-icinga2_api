## Instalation

Install https://github.com/L3viathan/icinga2api/tree/schedule-downtime-all-services to your Pyhton3 Lib Folder ~/.local/lib/python3.8/site-packages/


``` bash
mkdir -p ~/.ansible/plugins/modules

wget https://raw.githubusercontent.com/DoktorAerzt/ansible-icinga2_api/main/library/host_downtime.py -O ~/.ansible/plugins/modules/host_downtime.py
```

Create icinga_config for your environment

## Example
``` ansible
- name: Set Host Downtime
  hosts: localhost
  tasks:
  - name: run the new module
    host_downtime:
      host: FQDN
      config_file: /path/to/config_file
      api_endpoint: https://localhost:5665
    register: testout
  - name: dump test output
    debug:
      msg: '{{ testout }}'
```

## Options

options:
    host:
        description: Hostname for with the downtime should be set.
        required: true
        type: str
    config_file:
        description: Configfile for the icinga2 authentication.
        required: true
        type: str
    api_endpoint:
        description: Server FQDN. https://localhost:5665.
        required: true
        type: str
    downtime_author:
        description: Author of the Downtime, default ansible.
        required: false
        type: str
    downtime_comment:
        description: Description of the Downtime, default ansible generated.
        required: false
        type: str
    start_time:
        description: Starttime of the Downtime, default now. Format: Timestamp
        required: false
        type: int
    end_time:
        description: Endtime of the Downtime, default now + duration. Format: Timestamp
        required: false
        type: int
    duration:
        description: Duration in seconds of the Downtime, default 1000.
        required: false
        type: int
    fixed:
        description: Should the Downtime be Fixed, default true.
        required: false
        type: bool
    all_services:
        decription: Should the Downtime be for all services, default true.
        required: false
        type: bool 