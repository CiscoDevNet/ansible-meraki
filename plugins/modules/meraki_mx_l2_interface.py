#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: meraki_mx_l2_interface
short_description: Configure MX layer 2 interfaces
version_added: "2.1.0"
description:
- Allows for management and visibility of Merkai MX layer 2 ports.

options:
    state:
        description:
        - Create or modify an organization.
        choices: [present, query]
        default: present
        type: str
    net_name:
        description:
        - Name of a network.
        aliases: [name, network]
        type: str
    net_id:
        description:
        - ID number of a network.
        type: str
    org_id:
        description:
        - ID of organization associated to a network.
        type: str


author:
    - Kevin Breit (@kbreit)
extends_documentation_fragment: cisco.meraki.meraki
'''

EXAMPLES = r'''

'''

RETURN = r'''
data:
    description: Information about the created or manipulated object.
    returned: success
    type: complex
    contains:
        one_to_one:
            description: Information about 1:1 NAT object.
            returned: success, when 1:1 NAT object is in task
            type: complex
            contains:
'''

from ansible.module_utils.basic import AnsibleModule, json
from ansible.module_utils.common.dict_transformations import recursive_diff
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import MerakiModule, meraki_argument_spec


def main():

    # define the available arguments/parameters that a user can pass to
    # the module


    port_forwarding_spec = dict(name=dict(type='str'),
                                lan_ip=dict(type='str'),
                                uplink=dict(type='str', choices=['internet1', 'internet2', 'both']),
                                protocol=dict(type='str', choices=['tcp', 'udp']),
                                public_port=dict(type='int'),
                                local_port=dict(type='int'),
                                allowed_ips=dict(type='list', elements='str'),
                                )

    argument_spec = meraki_argument_spec()
    argument_spec.update(
        net_id=dict(type='str'),
        net_name=dict(type='str', aliases=['name', 'network']),
        state=dict(type='str', choices=['present', 'query'], default='present'),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )

    meraki = MerakiModule(module, function='mx_l2_interface')
    module.params['follow_redirects'] = 'all'

    get_all_urls = {'mx_l2_interface': '/networks/{net_id}/appliance/ports'}
    get_one_urls = {'mx_l2_interface': '/networks/{net_id}/appliance/ports/{port_id}'}
    update_urls = {'mx_l2_interface': '/networks/{net_id}/appliance/ports'}
    meraki.url_catalog['query_all'] = get_all_urls
    meraki.url_catalog['query_one'] = get_one_urls
    meraki.url_catalog['update'] = update_urls

    if meraki.params['net_name'] and meraki.params['net_id']:
        meraki.fail_json(msg='net_name and net_id are mutually exclusive')

    org_id = meraki.params['org_id']
    if not org_id:
        org_id = meraki.get_org_id(meraki.params['org_name'])
    net_id = meraki.params['net_id']
    if net_id is None:
        nets = meraki.get_nets(org_id=org_id)
        net_id = meraki.get_net_id(org_id, meraki.params['net_name'], data=nets)

    if meraki.params['state'] == 'query':
        if meraki.params['port'] is not None:
            path = meraki.construct_path('query_all', net_id=net_id, custom={'port_id': meraki.params['port_id']})
        else:
            path = meraki.construct_path('query_all', net_id=net_id)
        response = meraki.request(path, method='GET')
        meraki.result['data'] = response
        meraki.exit_json(**meraki.result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == '__main__':
    main()
