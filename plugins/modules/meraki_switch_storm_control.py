#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
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
module: meraki_switchport
short_description: Manage switchports on a switch in the Meraki cloud
version_added: "2.7"
description:
- Allows for management of switchports settings for Meraki MS switches.
options:
    state:
        description:
        - Specifies whether a switchport should be queried or modified.
        choices: [query, present]
        default: query
        type: str
    access_policy_number:
        description:
        - Number of the access policy to apply.
        - Only applicable to access port types.
        type: str
    allowed_vlans:
        description:
        - List of VLAN numbers to be allowed on switchport.
        default: all
        type: list
    enabled:
        description:
        - Whether a switchport should be enabled or disabled.
        type: bool
        default: yes
    isolation_enabled:
        description:
        - Isolation status of switchport.
        default: no
        type: bool
    link_negotiation:
        description:
        - Link speed for the switchport.
        default: Auto negotiate
        choices: [Auto negotiate, 100Megabit (auto), 100 Megabit full duplex (forced)]
        type: str
    name:
        description:
        - Switchport description.
        aliases: [description]
        type: str
    number:
        description:
        - Port number.
        type: str
    poe_enabled:
        description:
        - Enable or disable Power Over Ethernet on a port.
        type: bool
        default: true
    rstp_enabled:
        description:
        - Enable or disable Rapid Spanning Tree Protocol on a port.
        type: bool
        default: true
    serial:
        description:
        - Serial nubmer of the switch.
        type: str
    stp_guard:
        description:
        - Set state of STP guard.
        choices: [disabled, root guard, bpdu guard, loop guard]
        default: disabled
        type: str
    tags:
        description:
        - Space delimited list of tags to assign to a port.
        type: str
    type:
        description:
        - Set port type.
        choices: [access, trunk]
        default: access
        type: str
    vlan:
        description:
        - VLAN number assigned to port.
        - If a port is of type trunk, the specified VLAN is the native VLAN.
        type: int
    voice_vlan:
        description:
        - VLAN number assigned to a port for voice traffic.
        - Only applicable to access port type.
        type: int

author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: meraki
'''

EXAMPLES = r'''
- name: Query information about all switchports on a switch
  meraki_switchport:
    auth_key: abc12345
    state: query
    serial: ABC-123
  delegate_to: localhost

- name: Query information about all switchports on a switch
  meraki_switchport:
    auth_key: abc12345
    state: query
    serial: ABC-123
    number: 2
  delegate_to: localhost

- name: Name switchport
  meraki_switchport:
    auth_key: abc12345
    state: present
    serial: ABC-123
    number: 7
    name: Test Port
  delegate_to: localhost

- name: Configure access port with voice VLAN
  meraki_switchport:
    auth_key: abc12345
    state: present
    serial: ABC-123
    number: 7
    enabled: true
    name: Test Port
    tags: desktop
    type: access
    vlan: 10
    voice_vlan: 11
  delegate_to: localhost

- name: Check access port for idempotency
  meraki_switchport:
    auth_key: abc12345
    state: present
    serial: ABC-123
    number: 7
    enabled: true
    name: Test Port
    tags: desktop
    type: access
    vlan: 10
    voice_vlan: 11
  delegate_to: localhost

- name: Configure trunk port with specific VLANs
  meraki_switchport:
    auth_key: abc12345
    state: present
    serial: ABC-123
    number: 7
    enabled: true
    name: Server port
    tags: server
    type: trunk
    allowed_vlans:
      - 10
      - 15
      - 20
  delegate_to: localhost
'''

RETURN = r'''
data:
    description: Information queried or updated switchports.
    returned: success
    type: complex
    contains:
        number:
            description: Number of port.
            returned: success
            type: int
            sample: 1
        name:
            description: Human friendly description of port.
            returned: success
            type: str
            sample: "Jim Phone Port"
        tags:
            description: Space delimited list of tags assigned to port.
            returned: success
            type: str
            sample: phone marketing
        enabled:
            description: Enabled state of port.
            returned: success
            type: bool
            sample: true
        poe_enabled:
            description: Power Over Ethernet enabled state of port.
            returned: success
            type: bool
            sample: true
        type:
            description: Type of switchport.
            returned: success
            type: str
            sample: trunk
        vlan:
            description: VLAN assigned to port.
            returned: success
            type: int
            sample: 10
        voice_vlan:
            description: VLAN assigned to port with voice VLAN enabled devices.
            returned: success
            type: int
            sample: 20
        isolation_enabled:
            description: Port isolation status of port.
            returned: success
            type: bool
            sample: true
        rstp_enabled:
            description: Enabled or disabled state of Rapid Spanning Tree Protocol (RSTP)
            returned: success
            type: bool
            sample: true
        stp_guard:
            description: State of STP guard
            returned: success
            type: str
            sample: "Root Guard"
        access_policy_number:
            description: Number of assigned access policy. Only applicable to access ports.
            returned: success
            type: int
            sample: 1234
        link_negotiation:
            description: Link speed for the port.
            returned: success
            type: str
            sample: "Auto negotiate"
'''

from ansible.module_utils.basic import AnsibleModule, json
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import MerakiModule, meraki_argument_spec


def main():
    # define the available arguments/parameters that a user can pass to
    # the module
    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['present', 'query'], default='query'),
                         net_name=dict(type='str'),
                         net_id=dict(type='str'),
                         )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )
    meraki = MerakiModule(module, function='switch_storm_control')
    meraki.params['follow_redirects'] = 'all'

    query_urls = {'switch_storm_control': '/networks/{net_id}/switch/settings/stormControl'}
    update_url = {'switch_storm_control': '/networks/{net_id}/switchPorts/{number}'}

    meraki.url_catalog['get_all'].update(query_urls)
    meraki.url_catalog['update'] = update_url

    payload = None

    org_id = meraki.params['org_id']
    if not org_id:
        org_id = meraki.get_org_id(meraki.params['org_name'])
    net_id = meraki.params['net_id']
    if net_id is None:
        nets = meraki.get_nets(org_id=org_id)
        net_id = meraki.get_net_id(net_name=meraki.params['net_name'], data=nets)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    # FIXME: Work with Meraki so they can implement a check mode
    if module.check_mode:
        meraki.exit_json(**meraki.result)

    # execute checks for argument completeness

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    if meraki.params['state'] == 'query':
        path = meraki.construct_path('get_all', net_id=net_id)
        response = meraki.request(path, method='GET')
        if meraki.status == 200:
            meraki.result['data'] = response

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == '__main__':
    main()
