#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, 2019 Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
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
module: meraki_alert
version_added: "2.1.0"
short_description: Manage alerts in the Meraki cloud
description:
- Allows for creation, management, and visibility into alert settings within Meraki.
options:
    state:
        description:
        - Create or modify an alert.
        choices: [ present, query ]
        default: present
        type: str
    net_name:
        description:
        - Name of a network.
        aliases: [ name, network ]
        type: str
    net_id:
        description:
        - ID number of a network.
        type: str
    default_destinations:
        description:
        - Properties for destinations when alert specific destinations aren't specified.
        type: dict
        suboptions:
            all_admins:
                description:
                - If true, all network admins will receive emails.
                type: bool
            snmp:
                description:
                - If true, then an SNMP trap will be sent if there is an SNMP trap server configured for this network.
                type: bool
            emails:
                description:
                - A list of emails that will recieve the alert(s).
                type: list
                elements: str
            http_server_ids:
                description:
                - A list of HTTP server IDs to send a Webhook to.
                type: list
                elements: str
    alerts:
        description:
        - Alert-specific configuration for each type.
        type: list
        elements: dict
        suboptions:
            alert_type:
                description:
                - The type of alert.
                type: str
            enabled:
                description:
                - A boolean depicting if the alert is turned on or off.
                type: bool
            filters:
                description:
                - A hash of specific configuration data for the alert. Only filters specific to the alert will be updated.
                - No validation checks occur against C(filters).
                type: raw
            alert_destinations:
                description:
                - A hash of destinations for this specific alert.
                type: dict
                suboptions:
                    all_admins:
                        description:
                        - If true, all network admins will receive emails.
                        type: bool
                    snmp:
                        description:
                        - If true, then an SNMP trap will be sent if there is an SNMP trap server configured for this network.
                        type: bool
                    emails:
                        description:
                        - A list of emails that will recieve the alert(s).
                        type: list
                        elements: str
                    http_server_ids:
                        description:
                        - A list of HTTP server IDs to send a Webhook to.
                        type: list
                        elements: str

author:
    - Kevin Breit (@kbreit)
extends_documentation_fragment: cisco.meraki.meraki
"""

EXAMPLES = r"""
- name: Update settings
  meraki_alert:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    state: present
    default_destinations:
      emails:
      - 'youremail@yourcorp'
      - 'youremail2@yourcorp'
      all_admins: yes
      snmp: no
    alerts:
      - alert_type: "gatewayDown"
        enabled: yes
        filters:
          timeout: 60
        alert_destinations:
          emails:
          - 'youremail@yourcorp'
          - 'youremail2@yourcorp'
          all_admins: yes
          snmp: no
      - alert_type: "usageAlert"
        enabled: yes
        filters:
          period: 1200
          threshold: 104857600
        alert_destinations:
          emails:
          - 'youremail@yourcorp'
          - 'youremail2@yourcorp'
          all_admins: yes
          snmp: no

- name: Query all settings
  meraki_alert:
    auth_key: abc123
    org_name: YourOrg
    net_name: YourNet
    state: query
  delegate_to: localhost
"""

RETURN = r"""
data:
    description: Information about the created or manipulated object.
    returned: info
    type: complex
    contains:
        default_destinations:
            description: Properties for destinations when alert specific destinations aren't specified.
            returned: success
            type: complex
            contains:
                all_admins:
                    description: If true, all network admins will receive emails.
                    type: bool
                    sample: true
                    returned: success
                snmp:
                    description: If true, then an SNMP trap will be sent if there is an SNMP trap server configured for this network.
                    type: bool
                    sample: true
                    returned: success
                emails:
                    description: A list of emails that will recieve the alert(s).
                    type: list
                    returned: success
                http_server_ids:
                    description: A list of HTTP server IDs to send a Webhook to.
                    type: list
                    returned: success
        alerts:
            description: Alert-specific configuration for each type.
            type: complex
            contains:
                alert_type:
                    description: The type of alert.
                    type: str
                    returned: success
                enabled:
                    description: A boolean depicting if the alert is turned on or off.
                    type: bool
                    returned: success
                filters:
                    description:
                    - A hash of specific configuration data for the alert. Only filters specific to the alert will be updated.
                    - No validation checks occur against C(filters).
                    type: complex
                    returned: success
                alert_destinations:
                    description: A hash of destinations for this specific alert.
                    type: complex
                    contains:
                        all_admins:
                            description: If true, all network admins will receive emails.
                            type: bool
                            returned: success
                        snmp:
                            description: If true, then an SNMP trap will be sent if there is an SNMP trap server configured for this network.
                            type: bool
                            returned: success
                        emails:
                            description: A list of emails that will recieve the alert(s).
                            type: list
                            returned: success
                        http_server_ids:
                            description: A list of HTTP server IDs to send a Webhook to.
                            type: list
                            returned: success
"""

import copy
from ansible.module_utils.basic import AnsibleModule, json
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import (
    MerakiModule,
    meraki_argument_spec,
)


def construct_payload(meraki, original):
    payload = copy.deepcopy(original)
    if meraki.params["default_destinations"] is not None:
        payload["defaultDestinations"].update(meraki.params["default_destinations"])
        payload["defaultDestinations"]["allAdmins"] = meraki.params[
            "default_destinations"
        ]["all_admins"]
        payload["defaultDestinations"]["httpServerIds"] = meraki.params[
            "default_destinations"
        ]["http_server_ids"]
        del payload["defaultDestinations"]["all_admins"]
        del payload["defaultDestinations"]["http_server_ids"]
    if meraki.params["alerts"] is not None:
        for alert in meraki.params["alerts"]:
            alert.update(meraki.convert_snake_to_camel(alert))
            del alert["alert_destinations"]
        for alert_want in meraki.params["alerts"]:
            for alert_have in payload["alerts"]:
                if alert_want["alert_type"] == alert_have["type"]:
                    alert_have.update(alert_want)
                    del alert_have["alert_type"]
                    del alert_have["alertType"]
    return payload


def main():

    # define the available arguments/parameters that a user can pass to
    # the module

    destinations_arg_spec = dict(
        all_admins=dict(type="bool"),
        snmp=dict(type="bool"),
        emails=dict(type="list", elements="str"),
        http_server_ids=dict(type="list", elements="str", default=[]),
    )

    alerts_arg_spec = dict(
        alert_type=dict(type="str"),
        enabled=dict(type="bool"),
        alert_destinations=dict(
            type="dict", default=None, options=destinations_arg_spec
        ),
        filters=dict(type="raw", default={}),
    )

    argument_spec = meraki_argument_spec()
    argument_spec.update(
        net_id=dict(type="str"),
        net_name=dict(type="str", aliases=["name", "network"]),
        state=dict(type="str", choices=["present", "query"], default="present"),
        default_destinations=dict(
            type="dict", default=None, options=destinations_arg_spec
        ),
        alerts=dict(type="list", elements="dict", options=alerts_arg_spec),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    meraki = MerakiModule(module, function="alert")
    module.params["follow_redirects"] = "all"

    query_urls = {"alert": "/networks/{net_id}/alerts/settings"}
    update_urls = {"alert": "/networks/{net_id}/alerts/settings"}
    meraki.url_catalog["get_all"].update(query_urls)
    meraki.url_catalog["update"] = update_urls

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    org_id = meraki.params["org_id"]
    if org_id is None:
        org_id = meraki.get_org_id(meraki.params["org_name"])
    net_id = meraki.params["net_id"]
    if net_id is None:
        nets = meraki.get_nets(org_id=org_id)
        net_id = meraki.get_net_id(net_name=meraki.params["net_name"], data=nets)

    if meraki.params["state"] == "query":
        path = meraki.construct_path("get_all", net_id=net_id)
        response = meraki.request(path, method="GET")
        if meraki.status == 200:
            meraki.result["data"] = response
        meraki.exit_json(**meraki.result)
    elif meraki.params["state"] == "present":
        path = meraki.construct_path("get_all", net_id=net_id)
        original = meraki.request(path, method="GET")
        payload = construct_payload(meraki, original)
        # meraki.fail_json(msg="Compare", original=original, payload=payload)
        # meraki.fail_json(msg=payload)
        if meraki.is_update_required(original, payload):
            if meraki.check_mode is True:
                meraki.generate_diff(original, payload)
                meraki.result["data"] = payload
                meraki.result["changed"] = True
                meraki.exit_json(**meraki.result)
            path = meraki.construct_path("update", net_id=net_id)
            response = meraki.request(path, method="PUT", payload=json.dumps(payload))
            if meraki.status == 200:
                meraki.generate_diff(original, payload)
                meraki.result["data"] = response
                meraki.result["changed"] = True
                meraki.exit_json(**meraki.result)
        else:
            meraki.result["data"] = original
            meraki.exit_json(**meraki.result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == "__main__":
    main()
