#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
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
module: meraki_ms_switchport
short_description: Manage switchports on a switch in the Meraki cloud
description:
- Allows for management of switchports settings for Meraki MS switches.
options:
    state:
        description:
        - Specifies whether a switchport should be queried or modified.
        choices: [query, present]
        default: query
        type: str
    access_policy_type:
        description:
        - Type of access policy to apply to port.
        type: str
        choices: [Open, Custom access policy, MAC whitelist, Sticky MAC whitelist]
    access_policy_number:
        description:
        - Number of the access policy to apply.
        - Only applicable to access port types.
        type: int
    allowed_vlans:
        description:
        - List of VLAN numbers to be allowed on switchport.
        default: all
        type: list
        elements: str
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
        required: true
    stp_guard:
        description:
        - Set state of STP guard.
        choices: [disabled, root guard, bpdu guard, loop guard]
        default: disabled
        type: str
    tags:
        description:
        - List of tags to assign to a port.
        type: list
        elements: str
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
extends_documentation_fragment: cisco.meraki.meraki
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
            description: List of tags assigned to port.
            returned: success
            type: list
            sample: ['phone', 'marketing']
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

param_map = {'access_policy_number': 'accessPolicyNumber',
             'access_policy_type': 'accessPolicyType',
             'allowed_vlans': 'allowedVlans',
             'enabled': 'enabled',
             'isolation_enabled': 'isolationEnabled',
             'link_negotiation': 'linkNegotiation',
             'name': 'name',
             'number': 'number',
             'poe_enabled': 'poeEnabled',
             'rstp_enabled': 'rstpEnabled',
             'stp_guard': 'stpGuard',
             'tags': 'tags',
             'type': 'type',
             'vlan': 'vlan',
             'voice_vlan': 'voiceVlan',
             }


def sort_vlans(meraki, vlans):
    converted = set()
    for vlan in vlans:
        converted.add(int(vlan))
    vlans_sorted = sorted(converted)
    vlans_str = []
    for vlan in vlans_sorted:
        vlans_str.append(str(vlan))
    return ','.join(vlans_str)


def assemble_payload(meraki):
    payload = dict()
    # if meraki.params['enabled'] is not None:
    #     payload['enabled'] = meraki.params['enabled']

    for k, v in meraki.params.items():
        try:
            if meraki.params[k] is not None:
                if k == 'access_policy_number':
                    if meraki.params['access_policy_type'] is not None:
                        payload[param_map[k]] = v
                else:
                    payload[param_map[k]] = v
        except KeyError:
            pass
    return payload


def main():
    # define the available arguments/parameters that a user can pass to
    # the module
    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['present', 'query'], default='query'),
                         serial=dict(type='str', required=True),
                         number=dict(type='str'),
                         name=dict(type='str', aliases=['description']),
                         tags=dict(type='list', elements='str'),
                         enabled=dict(type='bool', default=True),
                         type=dict(type='str', choices=['access', 'trunk'], default='access'),
                         vlan=dict(type='int'),
                         voice_vlan=dict(type='int'),
                         allowed_vlans=dict(type='list', elements='str', default='all'),
                         poe_enabled=dict(type='bool', default=True),
                         isolation_enabled=dict(type='bool', default=False),
                         rstp_enabled=dict(type='bool', default=True),
                         stp_guard=dict(type='str', choices=['disabled', 'root guard', 'bpdu guard', 'loop guard'], default='disabled'),
                         access_policy_type=dict(type='str', choices=['Open', 'Custom access policy', 'MAC whitelist', 'Sticky MAC whitelist']),
                         access_policy_number=dict(type='int'),
                         link_negotiation=dict(type='str',
                                               choices=['Auto negotiate', '100Megabit (auto)', '100 Megabit full duplex (forced)'],
                                               default='Auto negotiate'),
                         )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )
    meraki = MerakiModule(module, function='switchport')
    meraki.params['follow_redirects'] = 'all'

    if meraki.params['type'] == 'trunk':
        if not meraki.params['allowed_vlans']:
            meraki.params['allowed_vlans'] = ['all']  # Backdoor way to set default without conflicting on access

    query_urls = {'switchport': '/devices/{serial}/switch/ports'}
    query_url = {'switchport': '/devices/{serial}/switch/ports/{number}'}
    update_url = {'switchport': '/devices/{serial}/switch/ports/{number}'}

    meraki.url_catalog['get_all'].update(query_urls)
    meraki.url_catalog['get_one'].update(query_url)
    meraki.url_catalog['update'] = update_url

    # execute checks for argument completeness

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    if meraki.params['state'] == 'query':
        if meraki.params['number']:
            path = meraki.construct_path('get_one', custom={'serial': meraki.params['serial'],
                                                            'number': meraki.params['number'],
                                                            })
            response = meraki.request(path, method='GET')
            meraki.result['data'] = response
        else:
            path = meraki.construct_path('get_all', custom={'serial': meraki.params['serial']})
            response = meraki.request(path, method='GET')
            meraki.result['data'] = response
    elif meraki.params['state'] == 'present':
        payload = assemble_payload(meraki)
        # meraki.fail_json(msg='payload', payload=payload)
        allowed = set()  # Use a set to remove duplicate items
        if meraki.params['allowed_vlans'][0] == 'all':
            allowed.add('all')
        else:
            for vlan in meraki.params['allowed_vlans']:
                allowed.add(str(vlan))
            if meraki.params['vlan'] is not None:
                allowed.add(str(meraki.params['vlan']))
        if len(allowed) > 1:  # Convert from list to comma separated
            payload['allowedVlans'] = sort_vlans(meraki, allowed)
        else:
            payload['allowedVlans'] = next(iter(allowed))

        # Exceptions need to be made for idempotency check based on how Meraki returns
        if meraki.params['type'] == 'access':
            if not meraki.params['vlan']:  # VLAN needs to be specified in access ports, but can't default to it
                payload['vlan'] = 1

        proposed = payload.copy()
        query_path = meraki.construct_path('get_one', custom={'serial': meraki.params['serial'],
                                                              'number': meraki.params['number'],
                                                              })
        original = meraki.request(query_path, method='GET')
        if meraki.params['type'] == 'trunk':
            proposed['voiceVlan'] = original['voiceVlan']  # API shouldn't include voice VLAN on a trunk port
        # meraki.fail_json(msg='Compare', original=original, payload=payload)
        if meraki.is_update_required(original, proposed, optional_ignore=['number']):
            if meraki.check_mode is True:
                original.update(proposed)
                meraki.result['data'] = original
                meraki.result['changed'] = True
                meraki.exit_json(**meraki.result)
            path = meraki.construct_path('update', custom={'serial': meraki.params['serial'],
                                                           'number': meraki.params['number'],
                                                           })
            # meraki.fail_json(msg=payload)
            response = meraki.request(path, method='PUT', payload=json.dumps(payload))
            meraki.result['data'] = response
            meraki.result['changed'] = True
        else:
            meraki.result['data'] = original

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == '__main__':
    main()
