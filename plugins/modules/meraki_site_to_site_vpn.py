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
module: meraki_site_to_site_vpn
short_description: Manage AutoVPN connections in Meraki
version_added: "2.10"
description:
- Allows for creation, management, and visibility into AutoVPNs implemented on Meraki MX firewalls.
options:
    state:
        description:
        - Create or modify an organization.
        choices: ['present', 'query']
        default: present
        type: str
    net_name:
        description:
        - Name of network which MX firewall is in.
        type: str
    net_id:
        description:
        - ID of network which MX firewall is in.
        type: str
    rules:
        description:
        - List of firewall rules.
        type: list
        suboptions:
            policy:
                description:
                - Policy to apply if rule is hit.
                choices: [allow, deny]
                type: str
            protocol:
                description:
                - Protocol to match against.
                choices: [any, icmp, tcp, udp]
                type: str
            dest_port:
                description:
                - Comma separated list of destination port numbers to match against.
                - C(Any) must be capitalized.
                type: str
            dest_cidr:
                description:
                - Comma separated list of CIDR notation destination networks.
                - C(Any) must be capitalized.
                type: str
            src_port:
                description:
                - Comma separated list of source port numbers to match against.
                - C(Any) must be capitalized.
                type: str
            src_cidr:
                description:
                - Comma separated list of CIDR notation source networks.
                - C(Any) must be capitalized.
                type: str
            comment:
                description:
                - Optional comment to describe the firewall rule.
                type: str
            syslog_enabled:
                description:
                - Whether to log hints against the firewall rule.
                - Only applicable if a syslog server is specified against the network.
                type: bool
    syslog_default_rule:
        description:
        - Whether to log hits against the default firewall rule.
        - Only applicable if a syslog server is specified against the network.
        - This is not shown in response from Meraki. Instead, refer to the C(syslog_enabled) value in the default rule.
        type: bool
        default: no
author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: meraki
'''

EXAMPLES = r'''
- name: Query firewall rules
  meraki_mx_l3_firewall:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    state: query
  delegate_to: localhost

- name: Set two firewall rules
  meraki_mx_l3_firewall:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    state: present
    rules:
      - comment: Block traffic to server
        src_cidr: 192.0.1.0/24
        src_port: any
        dest_cidr: 192.0.2.2/32
        dest_port: any
        protocol: any
        policy: deny
      - comment: Allow traffic to group of servers
        src_cidr: 192.0.1.0/24
        src_port: any
        dest_cidr: 192.0.2.0/24
        dest_port: any
        protocol: any
        policy: permit
  delegate_to: localhost

- name: Set one firewall rule and enable logging of the default rule
  meraki_mx_l3_firewall:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    state: present
    rules:
      - comment: Block traffic to server
        src_cidr: 192.0.1.0/24
        src_port: any
        dest_cidr: 192.0.2.2/32
        dest_port: any
        protocol: any
        policy: deny
    syslog_default_rule: yes
  delegate_to: localhost
'''

RETURN = r'''
data:
    description: Firewall rules associated to network.
    returned: success
    type: complex
    contains:
        comment:
            description: Comment to describe the firewall rule.
            returned: always
            type: str
            sample: Block traffic to server
        src_cidr:
            description: Comma separated list of CIDR notation source networks.
            returned: always
            type: str
            sample: 192.0.1.1/32,192.0.1.2/32
        src_port:
            description: Comma separated list of source ports.
            returned: always
            type: str
            sample: 80,443
        dest_cidr:
            description: Comma separated list of CIDR notation destination networks.
            returned: always
            type: str
            sample: 192.0.1.1/32,192.0.1.2/32
        dest_port:
            description: Comma separated list of destination ports.
            returned: always
            type: str
            sample: 80,443
        protocol:
            description: Network protocol for which to match against.
            returned: always
            type: str
            sample: tcp
        policy:
            description: Action to take when rule is matched.
            returned: always
            type: str
        syslog_enabled:
            description: Whether to log to syslog when rule is matched.
            returned: always
            type: bool
            sample: true
'''

from ansible.module_utils.basic import AnsibleModule, json
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import MerakiModule, meraki_argument_spec


def assemble_payload(meraki):
    payload = {'mode': meraki.params['mode']}
    if meraki.params['hubs'] is not None:
        payload['hubs'] = meraki.params['hubs']
        for hub in payload['hubs']:
            hub['hubId'] = hub.pop('hub_id')
            hub['useDefaultRoute'] = hub.pop('use_default_route')
    if meraki.params['subnets'] is not None:
        payload['subnets'] = meraki.params['subnets']
        for subnet in payload['subnets']:
            subnet['localSubnet'] = subnet.pop('local_subnet')
            subnet['useVpn'] = subnet.pop('use_vpn')
    return payload

def main():
    # define the available arguments/parameters that a user can pass to
    # the module

    hubs_args = dict(hub_id=dict(type='str'),
                     use_default_route=dict(type='bool'),
                     )
    subnets_args = dict(local_subnet=dict(type='str'),
                        use_vpn=dict(type='bool'),
                        )

    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['present', 'query'], default='present'),
                         net_name=dict(type='str'),
                         net_id=dict(type='str'),
                         hubs=dict(type='list', default=None, elements='dict', options=hubs_args),
                         subnets=dict(type='list', default=None, elements='dict', options=subnets_args),
                         mode=dict(type='str', choices=['none', 'hub', 'spoke']),
                         )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )
    meraki = MerakiModule(module, function='site_to_site_vpn')

    meraki.params['follow_redirects'] = 'all'

    query_urls = {'site_to_site_vpn': '/networks/{net_id}/siteToSiteVpn/'}
    update_urls = {'site_to_site_vpn': '/networks/{net_id}/siteToSiteVpn/'}

    meraki.url_catalog['get_all'].update(query_urls)
    meraki.url_catalog['update'] = update_urls

    payload = None

    # execute checks for argument completeness

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    org_id = meraki.params['org_id']
    if org_id is None:
        orgs = meraki.get_orgs()
        for org in orgs:
            if org['name'] == meraki.params['org_name']:
                org_id = org['id']
    net_id = meraki.params['net_id']
    if net_id is None:
        net_id = meraki.get_net_id(net_name=meraki.params['net_name'],
                                   data=meraki.get_nets(org_id=org_id))

    if meraki.params['state'] == 'query':
        path = meraki.construct_path('get_all', net_id=net_id)
        response = meraki.request(path, method='GET')
        meraki.result['data'] = response
    elif meraki.params['state'] == 'present':
        payload = assemble_payload(meraki)
        # meraki.fail_json(payload)
        path = meraki.construct_path('update', net_id=net_id)
        response = meraki.request(path, method='PUT', payload=json.dumps(payload))
        meraki.result['data'] = response

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == '__main__':
    main()
