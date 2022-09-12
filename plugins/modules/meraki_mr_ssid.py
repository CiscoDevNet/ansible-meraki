#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: meraki_mr_ssid
short_description: Manage wireless SSIDs in the Meraki cloud
description:
- Allows for management of SSIDs in a Meraki wireless environment.
notes:
- Deleting an SSID does not delete RADIUS servers.
options:
    state:
        description:
        - Specifies whether SNMP information should be queried or modified.
        type: str
        choices: [ absent, query, present ]
        default: present
    number:
        description:
        - SSID number within network.
        type: int
        aliases: [ssid_number]
    name:
        description:
        - Name of SSID.
        type: str
    net_name:
        description:
        - Name of network.
        type: str
    net_id:
        description:
        - ID of network.
        type: str
    enabled:
        description:
        - Enable or disable SSID network.
        type: bool
    auth_mode:
        description:
        - Set authentication mode of network.
        type: str
        choices: [open, psk, open-with-radius, 8021x-meraki, 8021x-radius]
    encryption_mode:
        description:
        - Set encryption mode of network.
        type: str
        choices: [wpa, eap, wpa-eap]
    psk:
        description:
        - Password for wireless network.
        - Requires auth_mode to be set to psk.
        type: str
    wpa_encryption_mode:
        description:
        - Encryption mode within WPA specification.
        type: str
        choices: [WPA1 and WPA2, WPA2 only, WPA3 Transition Mode, WPA3 only]
    splash_page:
        description:
        - Set to enable splash page and specify type of splash.
        type: str
        choices: ['None',
                  'Click-through splash page',
                  'Billing',
                  'Password-protected with Meraki RADIUS',
                  'Password-protected with custom RADIUS',
                  'Password-protected with Active Directory',
                  'Password-protected with LDAP',
                  'SMS authentication',
                  'Systems Manager Sentry',
                  'Facebook Wi-Fi',
                  'Google OAuth',
                  'Sponsored guest',
                  'Cisco ISE']
    radius_servers:
        description:
        - List of RADIUS servers.
        type: list
        elements: dict
        suboptions:
            host:
                description:
                - IP address or hostname of RADIUS server.
                type: str
                required: true
            port:
                description:
                - Port number RADIUS server is listening to.
                type: int
            secret:
                description:
                - RADIUS password.
                - Setting password is not idempotent.
                type: str
    radius_proxy_enabled:
        description:
        - Enable or disable RADIUS Proxy on SSID.
        type: bool
    radius_coa_enabled:
        description:
        - Enable or disable RADIUS CoA (Change of Authorization) on SSID.
        type: bool
    radius_failover_policy:
        description:
        - Set client access policy in case RADIUS servers aren't available.
        type: str
        choices: [Deny access, Allow access]
    radius_load_balancing_policy:
        description:
        - Set load balancing policy when multiple RADIUS servers are specified.
        type: str
        choices: [Strict priority order, Round robin]
    radius_accounting_enabled:
        description:
        - Enable or disable RADIUS accounting.
        type: bool
    radius_accounting_servers:
        description:
        - List of RADIUS servers for RADIUS accounting.
        type: list
        elements: dict
        suboptions:
            host:
                description:
                - IP address or hostname of RADIUS server.
                type: str
                required: true
            port:
                description:
                - Port number RADIUS server is listening to.
                type: int
            secret:
                description:
                - RADIUS password.
                - Setting password is not idempotent.
                type: str
    ip_assignment_mode:
        description:
        - Method of which SSID uses to assign IP addresses.
        type: str
        choices: ['NAT mode',
                  'Bridge mode',
                  'Layer 3 roaming',
                  'Layer 3 roaming with a concentrator',
                  'VPN']
    lan_isolation_enabled:
        description:
        - Enable or disable Layer 2 Lan isolation.
        - Requires C(ip_assignment_mode) to be C(Bridge mode).
        type: bool
    use_vlan_tagging:
        description:
        - Set whether to use VLAN tagging.
        - Requires C(default_vlan_id) to be set.
        type: bool
    visible:
        description:
        - Enable or disable whether APs should broadcast this SSID.
        type: bool
    default_vlan_id:
        description:
        - Default VLAN ID.
        - Requires C(ip_assignment_mode) to be C(Bridge mode) or C(Layer 3 roaming).
        type: int
    vlan_id:
        description:
        - ID number of VLAN on SSID.
        - Requires C(ip_assignment_mode) to be C(ayer 3 roaming with a concentrator) or C(VPN).
        type: int
    ap_tags_vlan_ids:
        description:
        - List of VLAN tags.
        - Requires C(ip_assignment_mode) to be C(Bridge mode) or C(Layer 3 roaming).
        - Requires C(use_vlan_tagging) to be C(True).
        type: list
        elements: dict
        suboptions:
            tags:
                description:
                - List of AP tags.
                type: list
                elements: str
            vlan_id:
                description:
                - Numerical identifier that is assigned to the VLAN.
                type: int
    walled_garden_enabled:
        description:
        - Enable or disable walled garden functionality.
        type: bool
    walled_garden_ranges:
        description:
        - List of walled garden ranges.
        type: list
        elements: str
    available_on_all_aps:
        description:
        - Set whether all APs should broadcast the SSID or if it should be restricted to APs matching any availability tags.
        - Requires C(ap_availability_tags) to be defined when set to C(False).
        type: bool
    ap_availability_tags:
        description:
        - Set whether SSID will be broadcast by APs with tags matching any of the tags in this list.
        - Requires C(available_on_all_aps) to be C(false).
        type: list
        elements: str
    min_bitrate:
        description:
        - Minimum bitrate (Mbps) allowed on SSID.
        type: float
        choices: [1, 2, 5.5, 6, 9, 11, 12, 18, 24, 36, 48, 54]
    band_selection:
        description:
        - Set band selection mode.
        type: str
        choices: ['Dual band operation', '5 GHz band only', 'Dual band operation with Band Steering']
    per_client_bandwidth_limit_up:
        description:
        - Maximum bandwidth in Mbps devices on SSID can upload.
        type: int
    per_client_bandwidth_limit_down:
        description:
        - Maximum bandwidth in Mbps devices on SSID can download.
        type: int
    concentrator_network_id:
        description:
        - The concentrator to use for 'Layer 3 roaming with a concentrator' or 'VPN'.
        type: str
    enterprise_admin_access:
        description:
        - Whether SSID is accessible by enterprise administrators.
        type: str
        choices: ['access disabled', 'access enabled']
    splash_guest_sponsor_domains:
        description:
        - List of valid sponsor email domains for sponsored guest portal.
        type: list
        elements: str
author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: cisco.meraki.meraki
"""

EXAMPLES = r"""
- name: Enable and name SSID
  meraki_ssid:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_name: WiFi
    name: GuestSSID
    enabled: true
    visible: true
  delegate_to: localhost

- name: Set PSK with invalid encryption mode
  meraki_ssid:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_name: WiFi
    name: GuestSSID
    auth_mode: psk
    psk: abc1234
    encryption_mode: eap
  ignore_errors: yes
  delegate_to: localhost

- name: Configure RADIUS servers
  meraki_ssid:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_name: WiFi
    name: GuestSSID
    auth_mode: open-with-radius
    radius_servers:
      - host: 192.0.1.200
        port: 1234
        secret: abc98765
  delegate_to: localhost

- name: Enable click-through splash page
  meraki_ssid:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_name: WiFi
    name: GuestSSID
    splash_page: Click-through splash page
  delegate_to: localhost
"""

RETURN = r"""
data:
    description: List of wireless SSIDs.
    returned: success
    type: complex
    contains:
        number:
            description: Zero-based index number for SSIDs.
            returned: success
            type: int
            sample: 0
        name:
            description:
              - Name of wireless SSID.
              - This value is what is broadcasted.
            returned: success
            type: str
            sample: CorpWireless
        enabled:
            description: Enabled state of wireless network.
            returned: success
            type: bool
            sample: true
        splash_page:
            description: Splash page to show when user authenticates.
            returned: success
            type: str
            sample: Click-through splash page
        ssid_admin_accessible:
            description: Whether SSID is administratively accessible.
            returned: success
            type: bool
            sample: true
        auth_mode:
            description: Authentication method.
            returned: success
            type: str
            sample: psk
        psk:
            description: Secret wireless password.
            returned: success
            type: str
            sample: SecretWiFiPass
        encryption_mode:
            description: Wireless traffic encryption method.
            returned: success
            type: str
            sample: wpa
        wpa_encryption_mode:
            description: Enabled WPA versions.
            returned: success
            type: str
            sample: WPA2 only
        ip_assignment_mode:
            description: Wireless client IP assignment method.
            returned: success
            type: str
            sample: NAT mode
        min_bitrate:
            description: Minimum bitrate a wireless client can connect at.
            returned: success
            type: int
            sample: 11
        band_selection:
            description: Wireless RF frequency wireless network will be broadcast on.
            returned: success
            type: str
            sample: 5 GHz band only
        per_client_bandwidth_limit_up:
            description: Maximum upload bandwidth a client can use.
            returned: success
            type: int
            sample: 1000
        per_client_bandwidth_limit_down:
            description: Maximum download bandwidth a client can use.
            returned: success
            type: int
            sample: 0
"""

from ansible.module_utils.basic import AnsibleModule, json
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import (
    MerakiModule,
    meraki_argument_spec,
)


def get_available_number(data):
    for item in data:
        if "Unconfigured SSID" in item["name"]:
            return item["number"]
    return False


def get_ssid_number(name, data):
    for ssid in data:
        if name == ssid["name"]:
            return ssid["number"]
    return False


def get_ssids(meraki, net_id):
    path = meraki.construct_path("get_all", net_id=net_id)
    return meraki.request(path, method="GET")


def construct_payload(meraki):
    param_map = {
        "name": "name",
        "enabled": "enabled",
        "authMode": "auth_mode",
        "encryptionMode": "encryption_mode",
        "psk": "psk",
        "wpaEncryptionMode": "wpa_encryption_mode",
        "splashPage": "splash_page",
        "radiusServers": "radius_servers",
        "radiusProxyEnabled": "radius_proxy_enabled",
        "radiusCoaEnabled": "radius_coa_enabled",
        "radiusFailoverPolicy": "radius_failover_policy",
        "radiusLoadBalancingPolicy": "radius_load_balancing_policy",
        "radiusAccountingEnabled": "radius_accounting_enabled",
        "radiusAccountingServers": "radius_accounting_servers",
        "ipAssignmentMode": "ip_assignment_mode",
        "useVlanTagging": "use_vlan_tagging",
        "visible": "visible",
        "concentratorNetworkId": "concentrator_network_id",
        "vlanId": "vlan_id",
        "lanIsolationEnabled": "lan_isolation_enabled",
        "availableOnAllAps": "available_on_all_aps",
        "availabilityTags": "ap_availability_tags",
        "defaultVlanId": "default_vlan_id",
        "apTagsAndVlanIds": "ap_tags_vlan_ids",
        "walledGardenEnabled": "walled_garden_enabled",
        "walledGardenRanges": "walled_garden_ranges",
        "minBitrate": "min_bitrate",
        "bandSelection": "band_selection",
        "perClientBandwidthLimitUp": "per_client_bandwidth_limit_up",
        "perClientBandwidthLimitDown": "per_client_bandwidth_limit_down",
        "enterpriseAdminAccess": "enterprise_admin_access",
        "splashGuestSponsorDomains": "splash_guest_sponsor_domains",
    }

    payload = dict()
    for k, v in param_map.items():
        if meraki.params[v] is not None:
            payload[k] = meraki.params[v]

    if meraki.params["ap_tags_vlan_ids"] is not None:
        for i in payload["apTagsAndVlanIds"]:
            try:
                i["vlanId"] = i["vlan_id"]
                del i["vlan_id"]
            except KeyError:
                pass

    return payload


def per_line_to_str(data):
    return data.replace("\n", " ")


def main():
    default_payload = {
        "name": "Unconfigured SSID",
        "auth_mode": "open",
        "splashPage": "None",
        "perClientBandwidthLimitUp": 0,
        "perClientBandwidthLimitDown": 0,
        "ipAssignmentMode": "NAT mode",
        "enabled": False,
        "bandSelection": "Dual band operation",
        "minBitrate": 11,
    }

    # define the available arguments/parameters that a user can pass to
    # the module
    radius_arg_spec = dict(
        host=dict(type="str", required=True),
        port=dict(type="int"),
        secret=dict(type="str", no_log=True),
    )
    vlan_arg_spec = dict(
        tags=dict(type="list", elements="str"),
        vlan_id=dict(type="int"),
    )

    argument_spec = meraki_argument_spec()
    argument_spec.update(
        state=dict(
            type="str", choices=["absent", "present", "query"], default="present"
        ),
        number=dict(type="int", aliases=["ssid_number"]),
        name=dict(type="str"),
        org_name=dict(type="str", aliases=["organization"]),
        org_id=dict(type="str"),
        net_name=dict(type="str"),
        net_id=dict(type="str"),
        enabled=dict(type="bool"),
        auth_mode=dict(
            type="str",
            choices=["open", "psk", "open-with-radius", "8021x-meraki", "8021x-radius"],
        ),
        encryption_mode=dict(type="str", choices=["wpa", "eap", "wpa-eap"]),
        psk=dict(type="str", no_log=True),
        wpa_encryption_mode=dict(
            type="str",
            choices=["WPA1 and WPA2", "WPA2 only", "WPA3 Transition Mode", "WPA3 only"],
        ),
        splash_page=dict(
            type="str",
            choices=[
                "None",
                "Click-through splash page",
                "Billing",
                "Password-protected with Meraki RADIUS",
                "Password-protected with custom RADIUS",
                "Password-protected with Active Directory",
                "Password-protected with LDAP",
                "SMS authentication",
                "Systems Manager Sentry",
                "Facebook Wi-Fi",
                "Google OAuth",
                "Sponsored guest",
                "Cisco ISE",
            ],
        ),
        radius_servers=dict(
            type="list", default=None, elements="dict", options=radius_arg_spec
        ),
        radius_proxy_enabled=dict(type="bool"),
        radius_coa_enabled=dict(type="bool"),
        radius_failover_policy=dict(
            type="str", choices=["Deny access", "Allow access"]
        ),
        radius_load_balancing_policy=dict(
            type="str", choices=["Strict priority order", "Round robin"]
        ),
        radius_accounting_enabled=dict(type="bool"),
        radius_accounting_servers=dict(
            type="list", elements="dict", options=radius_arg_spec
        ),
        ip_assignment_mode=dict(
            type="str",
            choices=[
                "NAT mode",
                "Bridge mode",
                "Layer 3 roaming",
                "Layer 3 roaming with a concentrator",
                "VPN",
            ],
        ),
        use_vlan_tagging=dict(type="bool"),
        visible=dict(type="bool"),
        lan_isolation_enabled=dict(type="bool"),
        available_on_all_aps=dict(type="bool"),
        ap_availability_tags=dict(type="list", elements="str"),
        concentrator_network_id=dict(type="str"),
        vlan_id=dict(type="int"),
        default_vlan_id=dict(type="int"),
        ap_tags_vlan_ids=dict(
            type="list", default=None, elements="dict", options=vlan_arg_spec
        ),
        walled_garden_enabled=dict(type="bool"),
        walled_garden_ranges=dict(type="list", elements="str"),
        min_bitrate=dict(
            type="float", choices=[1, 2, 5.5, 6, 9, 11, 12, 18, 24, 36, 48, 54]
        ),
        band_selection=dict(
            type="str",
            choices=[
                "Dual band operation",
                "5 GHz band only",
                "Dual band operation with Band Steering",
            ],
        ),
        per_client_bandwidth_limit_up=dict(type="int"),
        per_client_bandwidth_limit_down=dict(type="int"),
        enterprise_admin_access=dict(
            type="str", choices=["access disabled", "access enabled"]
        ),
        splash_guest_sponsor_domains=dict(type="list", elements="str"),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    meraki = MerakiModule(module, function="ssid")
    meraki.params["follow_redirects"] = "all"

    query_urls = {"ssid": "/networks/{net_id}/wireless/ssids"}
    query_url = {"ssid": "/networks/{net_id}/wireless/ssids/{number}"}
    update_url = {"ssid": "/networks/{net_id}/wireless/ssids/"}

    meraki.url_catalog["get_all"].update(query_urls)
    meraki.url_catalog["get_one"].update(query_url)
    meraki.url_catalog["update"] = update_url

    payload = None

    # execute checks for argument completeness
    if meraki.params["psk"]:
        if meraki.params["auth_mode"] != "psk":
            meraki.fail_json(msg="PSK is only allowed when auth_mode is set to psk")
        if meraki.params["encryption_mode"] != "wpa":
            meraki.fail_json(msg="PSK requires encryption_mode be set to wpa")
    if meraki.params["radius_servers"]:
        if meraki.params["auth_mode"] not in ("open-with-radius", "8021x-radius"):
            meraki.fail_json(
                msg="radius_servers requires auth_mode to be open-with-radius or 8021x-radius"
            )
    if meraki.params["radius_accounting_enabled"] is True:
        if meraki.params["auth_mode"] not in ("open-with-radius", "8021x-radius"):
            meraki.fail_json(
                msg="radius_accounting_enabled is only allowed when auth_mode is open-with-radius or 8021x-radius"
            )
    if meraki.params["radius_accounting_servers"] is True:
        if (
            meraki.params["auth_mode"] not in ("open-with-radius", "8021x-radius")
            or meraki.params["radius_accounting_enabled"] is False
        ):
            meraki.fail_json(
                msg="radius_accounting_servers is only allowed when auth_mode is open_with_radius or 8021x-radius and \
                radius_accounting_enabled is true"
            )
    if meraki.params["use_vlan_tagging"] is True:
        if meraki.params["default_vlan_id"] is None:
            meraki.fail_json(
                msg="default_vlan_id is required when use_vlan_tagging is True"
            )
    if meraki.params["lan_isolation_enabled"] is not None:
        if meraki.params["ip_assignment_mode"] not in ("Bridge mode"):
            meraki.fail_json(
                msg="lan_isolation_enabled is only allowed when ip_assignment_mode is Bridge mode"
            )
    if meraki.params["available_on_all_aps"] is False:
        if not meraki.params["ap_availability_tags"]:
            meraki.fail_json(
                msg="available_on_all_aps is only allowed to be false when ap_availability_tags is defined"
            )
    if meraki.params["ap_availability_tags"]:
        if meraki.params["available_on_all_aps"] is not False:
            meraki.fail_json(
                msg="ap_availability_tags is only allowed when available_on_all_aps is false"
            )
    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    org_id = meraki.params["org_id"]
    net_id = meraki.params["net_id"]
    if org_id is None:
        org_id = meraki.get_org_id(meraki.params["org_name"])
    if net_id is None:
        nets = meraki.get_nets(org_id=org_id)
        net_id = meraki.get_net_id(org_id, meraki.params["net_name"], data=nets)

    if meraki.params["state"] == "query":
        if meraki.params["name"]:
            ssid_id = get_ssid_number(meraki.params["name"], get_ssids(meraki, net_id))
            path = meraki.construct_path(
                "get_one", net_id=net_id, custom={"number": ssid_id}
            )
            meraki.result["data"] = meraki.request(path, method="GET")
        elif meraki.params["number"] is not None:
            path = meraki.construct_path(
                "get_one", net_id=net_id, custom={"number": meraki.params["number"]}
            )
            meraki.result["data"] = meraki.request(path, method="GET")
        else:
            meraki.result["data"] = get_ssids(meraki, net_id)
    elif meraki.params["state"] == "present":
        payload = construct_payload(meraki)
        ssids = get_ssids(meraki, net_id)
        number = meraki.params["number"]
        if number is None:
            number = get_ssid_number(meraki.params["name"], ssids)
        original = ssids[number]
        if meraki.is_update_required(original, payload, optional_ignore=["secret"]):
            ssid_id = meraki.params["number"]
            if ssid_id is None:  # Name should be used to lookup number
                ssid_id = get_ssid_number(meraki.params["name"], ssids)
                if ssid_id is False:
                    ssid_id = get_available_number(ssids)
                    if ssid_id is False:
                        meraki.fail_json(
                            msg="No unconfigured SSIDs are available. Specify a number."
                        )
            if meraki.check_mode is True:
                original.update(payload)
                meraki.result["data"] = original
                meraki.result["changed"] = True
                meraki.exit_json(**meraki.result)
            path = meraki.construct_path("update", net_id=net_id) + str(ssid_id)
            result = meraki.request(path, "PUT", payload=json.dumps(payload))
            meraki.result["data"] = result
            meraki.result["changed"] = True
        else:
            meraki.result["data"] = original
    elif meraki.params["state"] == "absent":
        ssids = get_ssids(meraki, net_id)
        ssid_id = meraki.params["number"]
        if ssid_id is None:  # Name should be used to lookup number
            ssid_id = get_ssid_number(meraki.params["name"], ssids)
            if ssid_id is False:
                # This will return True as long as there's an unclaimed SSID number!
                ssid_id = get_available_number(ssids)
                # There are no available SSIDs or SSID numbers
                if ssid_id is False:
                    meraki.fail_json(
                        msg="No SSID found by specified name and no numbers unclaimed."
                    )
                meraki.result["changed"] = False
                meraki.result["data"] = {}
                meraki.exit_json(**meraki.result)
        if meraki.check_mode is True:
            meraki.result["data"] = {}
            meraki.result["changed"] = True
            meraki.exit_json(**meraki.result)
        path = meraki.construct_path("update", net_id=net_id) + str(ssid_id)
        payload = default_payload
        payload["name"] = payload["name"] + " " + str(ssid_id + 1)
        result = meraki.request(path, "PUT", payload=json.dumps(payload))
        meraki.result["data"] = result
        meraki.result["changed"] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == "__main__":
    main()
