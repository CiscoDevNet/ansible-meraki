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
version_added: "2.7"
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
        type: str
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
    serial_lldp_cdp:
        description:
        - Serial number of device to query LLDP/CDP information from.
        type: str
    lldp_cdp_timespan:
        description:
        - Timespan, in seconds, used to query LLDP and CDP information.
        - Must be less than 1 month.
        type: int
    serial_uplink:
        description:
        - Serial number of device to query uplink information from.
        type: str
    note:
        description:
        - Informational notes about a device.
        - Limited to 255 characters.
        version_added: '2.8'
        type: str


author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: meraki
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

import os
from ansible.module_utils.basic import AnsibleModule, json, env_fallback
from ansible.module_utils._text import to_native
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import MerakiModule, meraki_argument_spec


def format_tags(tags):
    return " {tags} ".format(tags=tags)


def is_device_claimed_net(serial, data):
    for device in data:
        if device['serial'] == serial:
            return True
    return False


def is_device_claimed_org(serial, data):
    for device in data:
        if device['serial'] == serial:
            return True
    return False


def get_org_devices(meraki, org_id):
    path = meraki.construct_path('get_all_org', org_id=org_id)
    response = meraki.request(path, method='GET')
    if meraki.status != 200:
        meraki.fail_json(msg='Failed to query all devices belonging to the organization')
    return response


def get_net_devices(meraki, net_id):
    path = meraki.construct_path('get_all', net_id=net_id)
    response = meraki.request(path, method='GET')
    if meraki.status != 200:
        meraki.fail_json(msg='Failed to query all devices belonging to the network')
    return response


def construct_payload(data):
    payload = {}
    if data['hostname'] is not None:
        payload['name'] = data['hostname']
    if data['tags'] is not None:
        payload['tags'] = format_tags(data['tags'])
    if data['lat'] is not None:
        payload['lat'] = data['lat']
    if data['lng'] is not None:
        payload['lng'] = data['lng']
    if data['address'] is not None:
        payload['address'] = data['address']
    if data['note'] is not None:
        payload['notes'] = data['note']
    if data['move_map_marker'] is not None:
        payload['moveMapMarker'] = data['move_map_marker']
    return payload


def main():

    # define the available arguments/parameters that a user can pass to
    # the module
    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['absent', 'present', 'query'], default='query'),
                         net_name=dict(type='str', aliases=['network']),
                         net_id=dict(type='str'),
                         serial=dict(type='str'),
                         serial_uplink=dict(type='str'),
                         serial_lldp_cdp=dict(type='str'),
                         lldp_cdp_timespan=dict(type='int'),
                         hostname=dict(type='str', aliases=['name']),
                         model=dict(type='str'),
                         tags=dict(type='str'),
                         lat=dict(type='float', aliases=['latitude']),
                         lng=dict(type='float', aliases=['longitude']),
                         address=dict(type='str'),
                         move_map_marker=dict(type='bool'),
                         note=dict(type='str'),
                         )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )
    meraki = MerakiModule(module, function='device')

    if meraki.params['serial_lldp_cdp'] and not meraki.params['lldp_cdp_timespan']:
        meraki.fail_json(msg='lldp_cdp_timespan is required when querying LLDP and CDP information')
    if meraki.params['net_name'] and meraki.params['net_id']:
        meraki.fail_json(msg='net_name and net_id are mutually exclusive')

    meraki.params['follow_redirects'] = 'all'

    query_urls = {'device': '/networks/{net_id}/devices'}
    query_org_urls = {'device': '/organizations/{org_id}/inventory'}
    query_device_urls = {'device': '/networks/{net_id}/devices/'}
    query_device_uplink_urls = {'device': '/networks/{net_id}/devices/{serial}/uplink'}
    query_device_lldp_urls = {'device': '/networks/{net_id}/devices/{serial}/lldp_cdp'}
    claim_device_urls = {'device': '/networks/{net_id}/devices/claim'}
    claim_org_urls = {'device': '/organizations/{org_id}/claim'}
    update_device_urls = {'device': '/networks/{net_id}/devices/{serial}'}
    remove_device_urls = {'device': '/networks/{net_id}/devices/{serial}/remove'}

    meraki.url_catalog['get_all'].update(query_urls)
    meraki.url_catalog['get_all_org'] = query_org_urls
    meraki.url_catalog['get_device'] = query_device_urls
    meraki.url_catalog['get_uplink'] = query_device_uplink_urls
    meraki.url_catalog['get_lldp'] = query_device_lldp_urls
    meraki.url_catalog['create'] = claim_device_urls
    meraki.url_catalog['claim_org'] = claim_org_urls
    meraki.url_catalog['update'] = update_device_urls
    meraki.url_catalog['remove'] = remove_device_urls

    payload = None

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    # FIXME: Work with Meraki so they can implement a check mode
    if module.check_mode:
        meraki.exit_json(**meraki.result)

    # execute checks for argument completeness
    if meraki.params['lldp_cdp_timespan'] is not None and meraki.params['lldp_cdp_timespan'] > 2592000:
        meraki.fail_json(msg="serial_lldp_cdp must be less than 2592000 seconds.")

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    org_id = meraki.params['org_id']
    if org_id is None:
        org_id = meraki.get_org_id(meraki.params['org_name'])
    net_id = None
    if meraki.params['net_id'] or meraki.params['net_name']:
        net_id = meraki.params['net_id']
        if net_id is None:
            nets = meraki.get_nets(org_id=org_id)
            net_id = meraki.get_net_id(net_name=meraki.params['net_name'], data=nets)

    if meraki.params['state'] == 'query':
        if net_id is not None:  # Query devices in a network
            if meraki.params['serial'] is not None:  # Get a single device
                path = meraki.construct_path("get_device", net_id=net_id, custom={'serial': meraki.params['serial']})
                response = meraki.request(path, method='GET')
            elif meraki.params['hostname'] is not None:  # Get a single device by hostname
                for device in get_net_devices(meraki, net_id):
                    if device['hostname'] == meraki.params['name']:
                        response = device
            elif meraki.params['model'] is not None:  # Get all devices in a network with a model
                response = [device for device in get_net_devices(meraki, net_id) if meraki.params['model'] == device['model'] ]
            elif meraki.params['serial_uplink'] is not None:
                path = meraki.construct_path("get_uplink", net_id=net_id, custom={'serial': meraki.params['serial_uplink']})
                response = meraki.request(path, method='GET')
            elif meraki.params['serial_lldp_cdp'] is not None:
                path = meraki.construct_path("get_lldp", net_id=net_id, custom={'serial': meraki.params['serial_lldp_cdp']},params={'timespan': meraki.params['lldp_cdp_timespan']})
                response = meraki.request(path, method='GET')
            else:  # Get all devices in a network
                path = meraki.construct_path("get_all", net_id=net_id)
                response = meraki.request(path, method='GET')
            meraki.result['data'] = response
            meraki.exit_json(**meraki.result)
        else:  # Query an organization
            path = meraki.construct_path('get_all_org', org_id=org_id)
            response = meraki.request(path, method='GET')
            if meraki.params['serial'] is not None:
                for device in response:
                    if device['serial'] == meraki.params['serial']:
                        meraki.result['data'] = device
            else:
                meraki.result['data'] = response
            meraki.exit_json(**meraki.result)
    elif meraki.params['state'] == 'present':
        if net_id is not None:  
            if is_device_claimed_net(meraki.params['serial'], get_net_devices(meraki, net_id)) is False:  # Claim into a network
                if meraki.check_mode is True:
                    meraki.result['data'] = payload
                    meraki.result['changed'] = True
                    meraki.exit_json(**meraki.result)
                payload = {'serial': meraki.params['serial']}
                path = meraki.construct_path('create', net_id=net_id)
                response = meraki.request(path, method='POST', payload=json.dumps(payload))
                if meraki.status == 200:
                    meraki.result['changed'] = True
                    meraki.result['data'] = response
            else:
                path = meraki.construct_path('get_device', net_id=net_id, custom={'serial': meraki.params['serial']})
                device = meraki.request(path, method='GET')
                payload = construct_payload(meraki.params)
                if len(payload) > 0:  # Additional parameters were passed so update is needed
                    if meraki.is_update_required(device[0], payload, optional_ignore=['moveMapMarker']):
                        if meraki.check_mode is True:
                            meraki.result['data'] = payload
                            meraki.result['changed'] = True
                            meraki.exit_json(**meraki.result)
                        path = meraki.construct_path('update', net_id=net_id, custom={'serial': meraki.params['serial']})
                        response = meraki.request(path, method='PUT', payload=json.dumps(payload))
                        if meraki.status == 200:
                            meraki.result['data'] = response
                            meraki.result['changed'] = True
                    else:
                        meraki.result['data'] = device
                else:
                    meraki.result['data'] = device
        else:  # Claim into an organization
            if is_device_claimed_org(meraki.params['serial'], get_org_devices(meraki, org_id)) is False:  # Device isn't in a network
                payload = {'serials': [meraki.params['serial']]}
                if meraki.check_mode is True:
                    meraki.result['data'] = payload
                    meraki.result['changed'] = True
                    meraki.exit_json(**meraki.result)
                path = meraki.construct_path('claim_org', org_id=org_id)
                response = meraki.request(path, method='POST', payload=json.dumps(payload))
                if meraki.status == 200:
                    meraki.result['changed'] = True
                    meraki.result['data'] = response
        meraki.exit_json(**meraki.result)
    elif meraki.params['state'] == 'absent':
        if is_device_claimed_net(meraki.params['serial'], get_net_devices(meraki, net_id)) is True:
            if meraki.check_mode is True:
                meraki.result['data'] = {}
                meraki.result['changed'] = True
                meraki.exit_json(**meraki.result)
            path = meraki.construct_path('remove', net_id=net_id, custom={'serial': meraki.params['serial']})
            response = meraki.request(path, method='POST')
            if meraki.status == 204:
                meraki.result['changed'] = True
        meraki.exit_json(**meraki.result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == '__main__':
    main()
