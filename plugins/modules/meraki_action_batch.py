#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
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
module: meraki_action_batch
short_description: Manage Action Batch jobs within the Meraki Dashboard.
description:
- Allows for management of Action Batch jobs for Meraki.
options:
    state:
        description:
        - Specifies whether to lookup, create, or delete an Action Batch job.
        choices: ['query', 'present', 'absent']
        default: present
        type: str
    net_name:
        description:
        - Name of network, if applicable
        type: str
    net_id:
        description:
        - ID of network, if applicable
        type: str
    action_batch_id:
        description:
        - ID of an existing Action Batch job
        type: str
    confirmed:
        description:
        - Whether job is to be executed
        type: bool
        default: False
    synchronous:
        description:
        - Whether job is a synchronous or asynchronous job
        type: bool
        default: True
    actions:
        description:
        - List of actions the job should execute
        type: list
        elements: dict
        suboptions:
            operation:
                description:
                - Operation type of action
                type: str
                choices: [
                    'create',
                    'destroy',
                    'update',
                    'claim',
                    'bind',
                    'split',
                    'unbind',
                    'combine',
                    'update_order',
                    'cycle',
                    'swap',
                    'assignSeats',
                    'move',
                    'moveSeats',
                    'renewSeats'
                ]
            resource:
                description:
                - Path to Action Batch resource
                type: str
            body:
                description:
                - Required body of action
                type: raw
author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: cisco.meraki.meraki
"""


EXAMPLES = r"""
"""

RETURN = r"""
data:
    description: Information about SNMP settings.
    type: complex
    returned: always
    contains:
        hostname:
            description: Hostname of SNMP server.
            returned: success and no network specified.
            type: str
            sample: n1.meraki.com
        peer_ips:
            description: Semi-colon delimited list of IPs which can poll SNMP information.
            returned: success and no network specified.
            type: str
            sample: 192.0.1.1
        port:
            description: Port number of SNMP.
            returned: success and no network specified.
            type: str
            sample: 16100
        v2c_enabled:
            description: Shows enabled state of SNMPv2c
            returned: success and no network specified.
            type: bool
            sample: true
        v3_enabled:
            description: Shows enabled state of SNMPv3
            returned: success and no network specified.
            type: bool
            sample: true
        v3_auth_mode:
            description: The SNMP version 3 authentication mode either MD5 or SHA.
            returned: success and no network specified.
            type: str
            sample: SHA
        v3_priv_mode:
            description: The SNMP version 3 privacy mode DES or AES128.
            returned: success and no network specified.
            type: str
            sample: AES128
        v2_community_string:
            description: Automatically generated community string for SNMPv2c.
            returned: When SNMPv2c is enabled and no network specified.
            type: str
            sample: o/8zd-JaSb
        v3_user:
            description: Automatically generated username for SNMPv3.
            returned: When SNMPv3c is enabled and no network specified.
            type: str
            sample: o/8zd-JaSb
        access:
            description: Type of SNMP access.
            type: str
            returned: success, when network specified
        community_string:
            description: SNMP community string. Only relevant if C(access) is set to C(community).
            type: str
            returned: success, when network specified
        users:
            description: Information about users with access to SNMP. Only relevant if C(access) is set to C(users).
            type: complex
            contains:
                username:
                    description: Username of user with access.
                    type: str
                    returned: success, when network specified
                passphrase:
                    description: Passphrase for user SNMP access.
                    type: str
                    returned: success, when network specified
"""

from ansible.module_utils.basic import AnsibleModule, json
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict
from ansible_collections.cisco.meraki.plugins.module_utils.network.meraki.meraki import (
    MerakiModule,
    meraki_argument_spec,
)


def _construct_payload(meraki):
    payload = dict()
    payload["confirmed"] = meraki.params["confirmed"]
    payload["synchronous"] = meraki.params["synchronous"]
    if meraki.params["actions"] is not None:  # No payload is specified for an update
        payload["actions"] = list()
        for action in meraki.params["actions"]:
            action_detail = dict()
            if action["resource"] is not None:
                action_detail["resource"] = action["resource"]
            if action["operation"] is not None:
                action_detail["operation"] = action["operation"]
            if action["body"] is not None:
                action_detail["body"] = action["body"]
            payload["actions"].append(action_detail)
    return payload


def main():

    # define the available arguments/parameters that a user can pass to
    # the module

    actions_arg_spec = dict(
        operation=dict(
            type="str",
            choices=[
                "create",
                "destroy",
                "update",
                "claim",
                "bind",
                "split",
                "unbind",
                "combine",
                "update_order",
                "cycle",
                "swap",
                "assignSeats",
                "move",
                "moveSeats",
                "renewSeats",
            ],
        ),
        resource=dict(type="str"),
        body=dict(type="raw"),
    )

    argument_spec = meraki_argument_spec()
    argument_spec.update(
        state=dict(
            type="str", choices=["present", "query", "absent"], default="present"
        ),
        net_name=dict(type="str"),
        net_id=dict(type="str"),
        action_batch_id=dict(type="str", default=None),
        confirmed=dict(type="bool", default=False),
        synchronous=dict(type="bool", default=True),
        actions=dict(
            type="list", default=None, elements="dict", options=actions_arg_spec
        ),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    meraki = MerakiModule(module, function="action_batch")
    meraki.params["follow_redirects"] = "all"

    query_urls = {"action_batch": "/organizations/{org_id}/actionBatches"}
    query_one_urls = {
        "action_batch": "/organizations/{org_id}/actionBatches/{action_batch_id}"
    }
    create_urls = {"action_batch": "/organizations/{org_id}/actionBatches"}
    update_urls = {
        "action_batch": "/organizations/{org_id}/actionBatches/{action_batch_id}"
    }
    delete_urls = {
        "action_batch": "/organizations/{org_id}/actionBatches/{action_batch_id}"
    }

    meraki.url_catalog["get_all"].update(query_urls)
    meraki.url_catalog["get_one"].update(query_one_urls)
    meraki.url_catalog["create"] = create_urls
    meraki.url_catalog["update"] = update_urls
    meraki.url_catalog["delete"] = delete_urls

    payload = None

    if not meraki.params["org_name"] and not meraki.params["org_id"]:
        meraki.fail_json(msg="org_name or org_id is required")

    org_id = meraki.params["org_id"]
    if org_id is None:
        org_id = meraki.get_org_id(meraki.params["org_name"])

    if meraki.params["state"] == "query":
        if meraki.params["action_batch_id"] is None:  # Get all Action Batches
            path = meraki.construct_path("get_all", org_id=org_id)
            response = meraki.request(path, method="GET")
            if meraki.status == 200:
                meraki.result["data"] = response
                meraki.exit_json(**meraki.result)
        elif meraki.params["action_batch_id"] is not None:  # Query one Action Batch job
            path = meraki.construct_path(
                "get_one",
                org_id=org_id,
                custom={"action_batch_id": meraki.params["action_batch_id"]},
            )
            response = meraki.request(path, method="GET")
            if meraki.status == 200:
                meraki.result["data"] = response
                meraki.exit_json(**meraki.result)
    elif meraki.params["state"] == "present":
        if meraki.params["action_batch_id"] is None:  # Create a new Action Batch job
            payload = _construct_payload(meraki)
            path = meraki.construct_path("create", org_id=org_id)
            response = meraki.request(path, method="POST", payload=json.dumps(payload))
            if meraki.status == 201:
                meraki.result["data"] = response
                meraki.result["changed"] = True
                meraki.exit_json(**meraki.result)
        elif meraki.params["action_batch_id"] is not None:
            path = meraki.construct_path(
                "get_one",
                org_id=org_id,
                custom={"action_batch_id": meraki.params["action_batch_id"]},
            )
            current = meraki.request(path, method="GET")
            payload = _construct_payload(meraki)
            if (
                meraki.params["actions"] is not None
            ):  # Cannot update the body once a job is submitted
                meraki.fail_json(msg="Body cannot be updated on existing job.")
            if (
                meraki.is_update_required(current, payload) is True
            ):  # Job needs to be modified
                path = meraki.construct_path(
                    "update",
                    org_id=org_id,
                    custom={"action_batch_id": meraki.params["action_batch_id"]},
                )
                response = meraki.request(
                    path, method="PUT", payload=json.dumps(payload)
                )
                if meraki.status == 200:
                    meraki.result["data"] = response
                    meraki.result["changed"] = True
                    meraki.exit_json(**meraki.result)
            else:  # Idempotent response
                meraki.result["data"] = current
                meraki.exit_json(**meraki.result)
    elif meraki.params["state"] == "absent":
        path = meraki.construct_path(
            "delete",
            org_id=org_id,
            custom={"action_batch_id": meraki.params["action_batch_id"]},
        )
        response = meraki.request(path, method="DELETE")
        if meraki.status == 204:
            meraki.result["data"] = response
            meraki.result["changed"] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    meraki.exit_json(**meraki.result)


if __name__ == "__main__":
    main()
