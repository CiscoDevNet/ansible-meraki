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
module: meraki_device
short_description: Manage devices in the Meraki cloud
description:
- Visibility into devices associated to a Meraki environment.
notes:
- This module does not support claiming of devices or licenses into a Meraki organization.
- More information about the Meraki API can be found at U(https://dashboard.meraki.com/api_docs).
- Some of the options are likely only used for developers within Meraki.
options:
    state:
        description:
        - Query an organization.
        choices: [absent, present, query]
        default: query
        type: str
    net_name:
        description:
        - Name of a network.
        aliases: [network]
        type: str
    net_id:
        description:
        - ID of a network.
        type: str
    serial:
        description:
        - Serial number of a device to query.
        type: str
    hostname:
        description:
        - Hostname of network device to search for.
        aliases: [name]
        type: str
    model:
        description:
        - Model of network device to search for.
        type: str
    tags:
        description:
        - Space delimited list of tags to assign to device.
        type: list
        elements: str
    lat:
        description:
        - Latitude of device's geographic location.
        - Use negative number for southern hemisphere.
        aliases: [latitude]
        type: float
    lng:
        description:
        - Longitude of device's geographic location.
        - Use negative number for western hemisphere.
        aliases: [longitude]
        type: float
    address:
        description:
        - Postal address of device's location.
        type: str
    move_map_marker:
        description:
        - Whether or not to set the latitude and longitude of a device based on the new address.
        - Only applies when C(lat) and C(lng) are not specified.
        type: bool
    lldp_cdp_timespan:
        description:
        - Timespan, in seconds, used to query LLDP and CDP information.
        - Must be less than 1 month.
        type: int
    note:
        description:
        - Informational notes about a device.
        - Limited to 255 characters.
        type: str
    query:
        description:
        - Specifies what information should be queried.
        type: str
        choices: [lldp_cdp, uplink]


author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: cisco.meraki.meraki
'''

EXAMPLES = r'''
- name: Query all devices in an organization.
  meraki_device:
    auth_key: abc12345
    org_name: YourOrg
    state: query
  delegate_to: localhost

- name: Query all devices in a network.
  meraki_device:
    auth_key: abc12345
    org_name: YourOrg
    net_name: YourNet
    state: query
  delegate_to: localhost

- name: Query a device by serial number.
  meraki_device:
    auth_key: abc12345
    org_name: YourOrg
    net_name: YourNet
    serial: ABC-123
    state: query
  delegate_to: localhost

- name: Lookup uplink information about a device.
  meraki_device:
    auth_key: abc12345
    org_name: YourOrg
    net_name: YourNet
    serial_uplink: ABC-123
    state: query
  delegate_to: localhost

- name: Lookup LLDP and CDP information about devices connected to specified device.
  meraki_device:
    auth_key: abc12345
    org_name: YourOrg
    net_name: YourNet
    serial_lldp_cdp: ABC-123
    state: query
  delegate_to: localhost

- name: Lookup a device by hostname.
  meraki_device:
    auth_key: abc12345
    org_name: YourOrg
    net_name: YourNet
    hostname: main-switch
    state: query
  delegate_to: localhost

- name: Query all devices of a specific model.
  meraki_device:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    model: MR26
    state: query
  delegate_to: localhost

- name: Update information about a device.
  meraki_device:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    state: present
    serial: '{{serial}}'
    name: mr26
    address: 1060 W. Addison St., Chicago, IL
    lat: 41.948038
    lng: -87.65568
    tags: recently-added
  delegate_to: localhost

- name: Claim a device into a network.
  meraki_device:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    serial: ABC-123
    state: present
  delegate_to: localhost

- name: Remove a device from a network.
  meraki_device:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    serial: ABC-123
    state: absent
  delegate_to: localhost
'''

RETURN = r'''
response:
    description: Data returned from Meraki dashboard.
    type: dict
    returned: info
'''

from ansible.module_utils.basic import AnsibleModule, json
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import MerakiModule, meraki_argument_spec

def construct_payload(params):
    payload = {}
    if params['net_ids'] is not None:
        payload['networkIds'] = params['net_ids']
    if params['serials'] is not None:
        payload['serials'] = params['serials']
    if params['statuses'] is not None:
        payload['statuses'] = params['statuses']
    if params['product_types'] is not None:
        payload['productTypes'] = params['product_types']
    if params['models'] is not None:
        payload['models'] = params['models']
    if params['tags'] is not None:
        payload['tags'] = params['tags']
    if params['tags_filter_type'] is not None:
        payload['tagsFilterType'] = params['tags_filter_type']
    return payload

def main():

    # define the available arguments/parameters that a user can pass to
    # the module
    argument_spec = meraki_argument_spec()
    argument_spec.update(net_ids=dict(type='list'),
                         serials=dict(type='list'),
                         statuses=dict(type='list', choices=['online', 'alerting', 'offline', 'dormant']),
                         product_types=dict(type='list'),
                         models=dict(type='list'),
                         tags=dict(type='list'),
                         tags_filter_type=dict(type='str'),
                         )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False,
                           )
    meraki = MerakiModule(module, function='device_statuses')
    meraki.params['follow_redirects'] = 'all'
    query_urls = {'device_statuses': '/organizations/{org_id}/devices/statuses'}

    meraki.url_catalog['get_all'] = query_urls

    payload = construct_payload(meraki.params)

    # execute checks for argument completeness

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    org_id = meraki.params['org_id']
    if org_id is None:
        org_id = meraki.get_org_id(meraki.params['org_name'])
    
    # meraki.fail_json(meraki.url_catalog)
    path = meraki.construct_path('get_all', org_id=org_id)
    meraki.result['data'] = meraki.request(path, method='GET', payload=json.dumps(payload))

    # if meraki.params['state'] == 'query':
    #     if meraki.params['net_name'] or meraki.params['net_id']:
    #         device = []
    #         if meraki.params['serial']:
    #             path = meraki.construct_path('get_device', net_id=net_id, custom={'serial': meraki.params['serial']})
    #             request = meraki.request(path, method='GET')
    #             device.append(request)
    #             meraki.result['data'] = device
    #             if meraki.params['query'] == 'uplink':
    #                 path = meraki.construct_path('get_device_uplink', net_id=net_id, custom={'serial': meraki.params['serial']})
    #                 meraki.result['data'] = (meraki.request(path, method='GET'))
    #             elif meraki.params['query'] == 'lldp_cdp':
    #                 if meraki.params['lldp_cdp_timespan'] > 2592000:
    #                     meraki.fail_json(msg='LLDP/CDP timespan must be less than a month (2592000 seconds)')
    #                 path = meraki.construct_path('get_device_lldp', net_id=net_id, custom={'serial': meraki.params['serial']})
    #                 path = path + '?timespan=' + str(meraki.params['lldp_cdp_timespan'])
    #                 device.append(meraki.request(path, method='GET'))
    #                 meraki.result['data'] = device
    #         elif meraki.params['hostname']:
    #             path = meraki.construct_path('get_all', net_id=net_id)
    #             devices = meraki.request(path, method='GET')
    #             for unit in devices:
    #                 try:
    #                     if unit['name'] == meraki.params['hostname']:
    #                         device.append(unit)
    #                         meraki.result['data'] = device
    #                 except KeyError:
    #                     pass
    #         elif meraki.params['model']:
    #             path = meraki.construct_path('get_all', net_id=net_id)
    #             devices = meraki.request(path, method='GET')
    #             device_match = []
    #             for device in devices:
    #                 if device['model'] == meraki.params['model']:
    #                     device_match.append(device)
    #             meraki.result['data'] = device_match
    #         else:
    #             path = meraki.construct_path('get_all', net_id=net_id)
    #             request = meraki.request(path, method='GET')
    #             meraki.result['data'] = request
    #     else:
    #         path = meraki.construct_path('get_all_org', org_id=org_id, params={'perPage': '1000'})
    #         devices = meraki.request(path, method='GET', pagination_items=1000)
    #         if meraki.params['serial']:
    #             for device in devices:
    #                 if device['serial'] == meraki.params['serial']:
    #                     meraki.result['data'] = device
    #         else:
    #             meraki.result['data'] = devices
    # elif meraki.params['state'] == 'present':
    #     device = []
    #     if net_id is None:  # Claim a device to an organization
    #         device_list = get_org_devices(meraki, org_id)
    #         if is_device_valid(meraki, meraki.params['serial'], device_list) is False:
    #             payload = {'serial': meraki.params['serial']}
    #             path = meraki.construct_path('bind_org', org_id=org_id)
    #             created_device = []
    #             created_device.append(meraki.request(path, method='POST', payload=json.dumps(payload)))
    #             meraki.result['data'] = created_device
    #             meraki.result['changed'] = True
    #     else:  # A device is assumed to be in an organization
    #         device_list = get_net_devices(meraki, net_id)
    #         if is_device_valid(meraki, meraki.params['serial'], device_list) is True:  # Device is in network, update
    #             query_path = meraki.construct_path('get_all', net_id=net_id)
    #             if is_device_valid(meraki, meraki.params['serial'], device_list):
    #                 payload = construct_payload(meraki.params)
    #                 query_path = meraki.construct_path('get_device', net_id=net_id, custom={'serial': meraki.params['serial']})
    #                 device_data = meraki.request(query_path, method='GET')
    #                 ignore_keys = ['lanIp', 'serial', 'mac', 'model', 'networkId', 'moveMapMarker', 'wan1Ip', 'wan2Ip']
    #                 if meraki.is_update_required(device_data, payload, optional_ignore=ignore_keys):
    #                     path = meraki.construct_path('update', custom={'serial': meraki.params['serial']})
    #                     updated_device = []
    #                     updated_device.append(meraki.request(path, method='PUT', payload=json.dumps(payload)))
    #                     meraki.result['data'] = updated_device
    #                     meraki.result['changed'] = True
    #                 else:
    #                     meraki.result['data'] = device_data
    #         else:  # Claim device into network
    #             query_path = meraki.construct_path('get_all', net_id=net_id)
    #             device_list = meraki.request(query_path, method='GET')
    #             if is_device_valid(meraki, meraki.params['serial'], device_list) is False:
    #                 if net_id:
    #                     payload = {'serials': [meraki.params['serial']]}
    #                     path = meraki.construct_path('create', net_id=net_id)
    #                     created_device = []
    #                     created_device.append(meraki.request(path, method='POST', payload=json.dumps(payload)))
    #                     meraki.result['data'] = created_device
    #                     meraki.result['changed'] = True
    # elif meraki.params['state'] == 'absent':
    #     device = []
    #     query_path = meraki.construct_path('get_all', net_id=net_id)
    #     device_list = meraki.request(query_path, method='GET')
    #     if is_device_valid(meraki, meraki.params['serial'], device_list) is True:
    #         payload = {'serial': meraki.params['serial']}
    #         path = meraki.construct_path('delete', net_id=net_id)
    #         request = meraki.request(path, method='POST', payload=json.dumps(payload))
    #         meraki.result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == '__main__':
    main()
