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
module: meraki_mr_l3_firewall
short_description: Manage MR access point layer 3 firewalls in the Meraki cloud
description:
- Allows for creation, management, and visibility into layer 3 firewalls implemented on Meraki MR access points.
- Module is not idempotent as of current release.
options:
    state:
        description:
        - Create or modify an organization.
        type: str
        choices: [ present, query ]
        default: present
    net_name:
        description:
        - Name of network containing access points.
        type: str
    net_id:
        description:
        - ID of network containing access points.
        type: str
    number:
        description:
        - Number of SSID to apply firewall rule to.
        type: str
        aliases: [ ssid_number ]
    ssid_name:
        description:
        - Name of SSID to apply firewall rule to.
        type: str
        aliases: [ ssid ]
    allow_lan_access:
        description:
        - Sets whether devices can talk to other devices on the same LAN.
        type: bool
        default: yes
    rules:
        description:
        - List of firewall rules.
        type: list
        elements: dict
        suboptions:
            policy:
                description:
                - Specifies the action that should be taken when rule is hit.
                type: str
                choices: [ allow, deny ]
            protocol:
                description:
                - Specifies protocol to match against.
                type: str
                choices: [ any, icmp, tcp, udp ]
            dest_port:
                description:
                - Comma-seperated list of destination ports to match.
                type: str
            dest_cidr:
                description:
                - Comma-separated list of CIDR notation networks to match.
                type: str
            comment:
                description:
                - Optional comment describing the firewall rule.
                type: str
author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: cisco.meraki.meraki
'''

EXAMPLES = r'''
- name: Create single firewall rule
  meraki_mr_l3_firewall:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_id: 12345
    number: 1
    rules:
      - comment: Integration test rule
        policy: allow
        protocol: tcp
        dest_port: 80
        dest_cidr: 192.0.2.0/24
    allow_lan_access: no
  delegate_to: localhost

- name: Enable local LAN access
  meraki_mr_l3_firewall:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_id: 123
    number: 1
    rules:
    allow_lan_access: yes
  delegate_to: localhost

- name: Query firewall rules
  meraki_mr_l3_firewall:
    auth_key: abc123
    state: query
    org_name: YourOrg
    net_name: YourNet
    number: 1
  delegate_to: localhost
'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule, json
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import MerakiModule, meraki_argument_spec


def assemble_payload(meraki):
    params_map = {'policy': 'policy',
                  'protocol': 'protocol',
                  'dest_port': 'destPort',
                  'dest_cidr': 'destCidr',
                  'comment': 'comment',
                  }
    rules = []
    for rule in meraki.params['rules']:
        proposed_rule = dict()
        for k, v in rule.items():
            proposed_rule[params_map[k]] = v
        rules.append(proposed_rule)
    payload = {'rules': rules}
    return payload


def get_rules(meraki, net_id, number):
    path = meraki.construct_path('get_all', net_id=net_id, custom={'number': number})
    response = meraki.request(path, method='GET')
    if meraki.status == 200:
        return response


def get_ssid_number(name, data):
    for ssid in data:
        if name == ssid['name']:
            return ssid['number']
    return False


def get_ssids(meraki, net_id):
    path = meraki.construct_path('get_all', net_id=net_id)
    return meraki.request(path, method='GET')


def main():
    # define the available arguments/parameters that a user can pass to
    # the module

    fw_rules = dict(policy=dict(type='str', choices=['allow', 'deny']),
                    protocol=dict(type='str', choices=['tcp', 'udp', 'icmp', 'any']),
                    dest_port=dict(type='str'),
                    dest_cidr=dict(type='str'),
                    comment=dict(type='str'),
                    )

    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['present', 'query'], default='present'),
                         net_name=dict(type='str'),
                         net_id=dict(type='str'),
                         number=dict(type='str', aliases=['ssid_number']),
                         ssid_name=dict(type='str', aliases=['ssid']),
                         rules=dict(type='list', default=None, elements='dict', options=fw_rules),
                         allow_lan_access=dict(type='bool', default=True),
                         )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )
    meraki = MerakiModule(module, function='mr_l3_firewall')

    meraki.params['follow_redirects'] = 'all'

    query_urls = {'mr_l3_firewall': '/networks/{net_id}/wireless/ssids/{number}/firewall/l3FirewallRules'}
    update_urls = {'mr_l3_firewall': '/networks/{net_id}/wireless/ssids/{number}/firewall/l3FirewallRules'}

    meraki.url_catalog['get_all'].update(query_urls)
    meraki.url_catalog['update'] = update_urls

    payload = None

    # execute checks for argument completeness

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    org_id = meraki.params['org_id']
    orgs = None
    if org_id is None:
        orgs = meraki.get_orgs()
        for org in orgs:
            if org['name'] == meraki.params['org_name']:
                org_id = org['id']
    net_id = meraki.params['net_id']
    if net_id is None:
        if orgs is None:
            orgs = meraki.get_orgs()
        net_id = meraki.get_net_id(net_name=meraki.params['net_name'],
                                   data=meraki.get_nets(org_id=org_id))
    number = meraki.params['number']
    if meraki.params['ssid_name']:
        number = get_ssid_number(meraki.params['ssid_name'], get_ssids(meraki, net_id))

    if meraki.params['state'] == 'query':
        meraki.result['data'] = get_rules(meraki, net_id, number)
    elif meraki.params['state'] == 'present':
        rules = get_rules(meraki, net_id, number)
        path = meraki.construct_path('get_all', net_id=net_id, custom={'number': number})
        if meraki.params['rules']:
            payload = assemble_payload(meraki)
        else:
            payload = dict()
        update = False
        try:
            if len(rules) != len(payload['rules']):  # Quick and simple check to avoid more processing
                update = True
            if update is False:
                for r in range(len(rules) - 2):
                    if meraki.is_update_required(rules[r], payload[r]) is True:
                        update = True
        except KeyError:
            pass
        # meraki.fail_json(msg=rules)
        if rules['rules'][len(rules['rules']) - 2] != meraki.params['allow_lan_access']:
            update = True
        if update is True:
            payload['allowLanAccess'] = meraki.params['allow_lan_access']
            if meraki.check_mode is True:
                # This code is disgusting, rework it at some point
                if 'rules' in payload:
                    cleansed_payload = payload['rules']
                    cleansed_payload.append(rules['rules'][len(rules['rules']) - 1])
                    cleansed_payload.append(rules['rules'][len(rules['rules']) - 2])
                    if meraki.params['allow_lan_access'] is None:
                        cleansed_payload[len(cleansed_payload) - 2]['policy'] = rules['rules'][len(rules['rules']) - 2]['policy']
                    else:
                        if meraki.params['allow_lan_access'] is True:
                            cleansed_payload[len(cleansed_payload) - 2]['policy'] = 'allow'
                        else:
                            cleansed_payload[len(cleansed_payload) - 2]['policy'] = 'deny'
                else:
                    if meraki.params['allow_lan_access'] is True:
                        rules['rules'][len(rules['rules']) - 2]['policy'] = 'allow'
                    else:
                        rules['rules'][len(rules['rules']) - 2]['policy'] = 'deny'
                    cleansed_payload = rules
                meraki.result['data'] = cleansed_payload
                meraki.result['changed'] = True
                meraki.exit_json(**meraki.result)
            response = meraki.request(path, method='PUT', payload=json.dumps(payload))
            if meraki.status == 200:
                meraki.result['data'] = response
                meraki.result['changed'] = True
        else:
            meraki.result['data'] = rules

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == '__main__':
    main()
