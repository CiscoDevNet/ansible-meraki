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
module: meraki_ms_static_route
short_description: Manage static routes on MS switches
description:
- Allows for creation, management, and visibility into static routes on Meraki MS switches.
options:
    state:
        description:
        - Create or modify an organization.
        type: str
        choices: [ present, query, absent ]
        default: present
    serial:
        description:
        - Serial number of MS switch.
        type: str
    name:
        description:
        - Name or description for layer 3 static route.
        type: str
    static_route_id:
        description:
        - Identification number of existing static route.
        type: str
    subnet:
        description:
        - The subnet which is routed via this static route and should be specified in CIDR notation (ex. 1.2.3.0/24).
        type: str
    next_hop_ip:
        description:
        - IP address of the next hop device to which the device sends its traffic for the subnet.
        type: str
    advertise_via_ospf_enabled:
        description:
        - Option to advertise static route via OSPF.
        type: bool
    prefer_over_ospf_routes_enabled:
        description:
        - Option to prefer static route over OSPF routes.
        type: bool
author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: cisco.meraki.meraki
'''

EXAMPLES = r'''
- name: Query all static routes on a switch
  meraki_ms_static_route:
    auth_key: abc123
    state: query
    serial: aaa-bbb-ccc
  delegate_to: localhost

- name: Query a single static route
  meraki_ms_static_route:
    auth_key: abc123
    state: query
    serial: aaa-bbb-ccc
    name: Test Route

- name: Create static route with check mode
  meraki_ms_static_route:
    auth_key: abc123
    state: present
    serial: aaa-bbb-ccc
    name: Test Route
    subnet: 192.168.17.0/24
    next_hop_ip: 192.168.2.1
  delegate_to: localhost

- name: Create static route
  meraki_ms_static_route:
    auth_key: abc123
    state: present
    serial: aaa-bbb-ccc
    name: Test Route
    subnet: 192.168.17.0/24
    next_hop_ip: 192.168.2.1
  delegate_to: localhost
'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule, json
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import MerakiModule, meraki_argument_spec


def construct_payload(meraki):
    payload = {}
    if meraki.params['name'] is not None:
        payload['name'] = meraki.params['name']
    if meraki.params['subnet'] is not None:
        payload['subnet'] = meraki.params['subnet']
    if meraki.params['next_hop_ip'] is not None:
        payload['nextHopIp'] = meraki.params['next_hop_ip']
    if meraki.params['advertise_via_ospf_enabled'] is not None:
        payload['advertiseViaOspfEnabled'] = meraki.params['advertise_via_ospf_enabled']
    if meraki.params['prefer_over_ospf_routes_enabled'] is not None:
        payload['preferOverOspfRoutesEnabled'] = meraki.params['prefer_over_ospf_routes_enabled']
    return payload


def get_static_route(static_routes, id):
    for route in static_routes:
        if route['staticRouteId'] == id:
            return route
    return None


def get_static_route_id(static_routes, name):
    for route in static_routes:
        if route['name'] == name:
            return route['staticRouteId']
    return None


def main():
    # define the available arguments/parameters that a user can pass to
    # the module
    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['present', 'query', 'absent'], default='present'),
                         serial=dict(type='str'),
                         name=dict(type='str'),
                         static_route_id=dict(type='str'),
                         subnet=dict(type='str'),
                         next_hop_ip=dict(type='str'),
                         advertise_via_ospf_enabled=dict(type='bool'),
                         prefer_over_ospf_routes_enabled=dict(type='bool'),
                         )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )
    meraki = MerakiModule(module, function='ms_static_route')

    meraki.params['follow_redirects'] = 'all'

    query_urls = {'ms_static_route': '/devices/{serial}/switch/routing/staticRoutes'}
    query_one_urls = {'ms_static_route': '/devices/{serial}/switch/routing/staticRoutes/{static_route_id}'}
    create_urls = {'ms_static_route': '/devices/{serial}/switch/routing/staticRoutes'}
    update_urls = {'ms_static_route': '/devices/{serial}/switch/routing/staticRoutes/{static_route_id}'}
    delete_urls = {'ms_static_route': '/devices/{serial}/switch/routing/staticRoutes/{static_route_id}'}

    meraki.url_catalog['get_all'].update(query_urls)
    meraki.url_catalog['get_one'].update(query_one_urls)
    meraki.url_catalog['create'] = create_urls
    meraki.url_catalog['update'] = update_urls
    meraki.url_catalog['delete'] = delete_urls

    payload = None

    static_route_id = meraki.params['static_route_id']
    static_routes = None
    if static_route_id is None:
        path = meraki.construct_path('get_all', custom={'serial': meraki.params['serial']})
        static_routes = meraki.request(path, method='GET')
        static_route_id = get_static_route_id(static_routes, meraki.params['name'])

    if meraki.params['state'] == 'query':
        if static_route_id is None:
            path = meraki.construct_path('get_all', custom={'serial': meraki.params['serial']})
            response = meraki.request(path, method='GET')
            meraki.result['data'] = response
        else:
            path = meraki.construct_path('get_one', custom={'serial': meraki.params['serial'],
                                                            'static_route_id': static_route_id})
            response = meraki.request(path, method='GET')
            meraki.result['data'] = response
        meraki.exit_json(**meraki.result)
    elif meraki.params['state'] == 'present':
        if static_route_id is None:  # Create new static route
            payload = construct_payload(meraki)
            if meraki.check_mode is True:
                meraki.result['data'] = payload
                meraki.result['changed'] = True
                meraki.exit_json(**meraki.result)
            path = meraki.construct_path('create', custom={'serial': meraki.params['serial']})
            response = meraki.request(path, method='POST', payload=json.dumps(payload))
            meraki.result['data'] = response
            meraki.result['changed'] = True
        else:  # Update existing static route
            if static_routes is None:
                path = meraki.construct_path('get_all', custom={'serial': meraki.params['serial']})
                static_routes = meraki.request(path, method='GET')
            original = get_static_route(static_routes, static_route_id)
            payload = construct_payload(meraki)
            if meraki.is_update_required(original, payload) is True:
                if meraki.check_mode is True:
                    original.update(payload)
                    meraki.result['data'] = original
                    meraki.result['changed'] = True
                    meraki.exit_json(**meraki.result)
                path = meraki.construct_path('update', custom={'serial': meraki.params['serial'],
                                                               'static_route_id': static_route_id})
                payload = construct_payload(meraki)
                response = meraki.request(path, method='PUT', payload=json.dumps(payload))
                meraki.result['data'] = response
                meraki.result['changed'] = True
            else:
                meraki.result['data'] = original
        meraki.exit_json(**meraki.result)
    elif meraki.params['state'] == 'absent':
        if meraki.check_mode is True:
            meraki.result['data'] = {}
            meraki.result['changed'] = True
            meraki.exit_json(**meraki.result)
        path = meraki.construct_path('delete', custom={'serial': meraki.params['serial'],
                                                       'static_route_id': static_route_id})
        response = meraki.request(path, method='DELETE')
        meraki.result['data'] = {}
        meraki.result['changed'] = True
        meraki.exit_json(**meraki.result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == '__main__':
    main()
