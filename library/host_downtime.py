#!/usr/bin/python

# Copyright: (c) 2023, Bohnet Michael <DoktorAerzt@github.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: host_downtime

short_description: This module sets downtime of a Host in Icinga2

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description: This module sets downtime of a Host in Icinga2

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
    
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - host_downtime

author:
    - Bohnet Michael (@DoktorAerzt)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
Nothing at the moment
'''

from ansible.module_utils.basic import AnsibleModule
#from icinga2api import icinga2api 
from icinga2api.client import Client
from datetime import datetime
import time


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        host=dict(type='str', required=True),
        config_file=dict(type='str', required=True),
        api_endpoint=dict(type='str', required=True),
        downtime_author=dict(type='str', required=False, default='ansible'),
        downtime_comment=dict(type='str', required=False, default='ansible generated'),
        start_time=dict(type='int', required=False, default=0), #Now
        end_time=dict(type='int', required=False, default=0), #start-time + duration
        duration=dict(type='int', required=False, default=1000),
        fixed=dict(type='bool', required=False, default=True),
        all_services=dict(type='bool', required=False, default=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        response=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if module.params['start_time'] == 0:
       start_time = int(time.mktime(datetime.now().timetuple()))

    if module.params['end_time'] == 0:
        end_time = start_time + module.params['duration']

    if module.params['end_time'] == start_time + module.params['duration']:
        module.fail_json(msg='start_time and duration != end_time', **result)

    print('host.name=="' + module.params['host'] + '"')


    client = Client(module.params['api_endpoint'], config_file=module.params['config_file'])
    #client = Client(module.params['api_endpoint'], "icingaweb", "icingaweb")
    result['response'] = client.actions.schedule_downtime(
        'Host',
        'host.name=="' + module.params['host'] + '"',
        module.params['downtime_author'],
        module.params['downtime_comment'],
        start_time,
        end_time,
        module.params['duration'],
        fixed=module.params['fixed'],
        all_services=module.params['all_services']
    )

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()


