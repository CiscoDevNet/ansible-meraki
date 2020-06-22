# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard files for documentation fragment
    DOCUMENTATION = r'''
notes:
- More information about the Meraki API can be found at U(https://dashboard.meraki.com/api_docs).
- Some of the options are likely only used for developers within Meraki.
- As of Ansible 2.9, Meraki modules output keys as snake case. To use camel case, set the C(ANSIBLE_MERAKI_FORMAT) environment variable to C(camelcase).
- Ansible's Meraki modules will stop supporting camel case output in Ansible 2.13. Please update your playbooks.
options:
    auth_key:
        description:
        - Authentication key provided by the dashboard. Required if environmental variable C(MERAKI_KEY) is not set.
        type: str
        required: yes
    host:
        description:
        - Hostname for Meraki dashboard.
        - Can be used to access regional Meraki environments, such as China.
        type: str
        default: api.meraki.com
    use_proxy:
        description:
        - If C(no), it will not use a proxy, even if one is defined in an environment variable on the target hosts.
        type: bool
    use_https:
        description:
        - If C(no), it will use HTTP. Otherwise it will use HTTPS.
        - Only useful for internal Meraki developers.
        type: bool
        default: yes
    output_format:
        description:
        - Instructs module whether response keys should be snake case (ex. C(net_id)) or camel case (ex. C(netId)).
        type: str
        choices: [snakecase, camelcase]
        default: snakecase
    output_level:
        description:
        - Set amount of debug output during module execution.
        type: str
        choices: [ debug, normal ]
        default: normal
    timeout:
        description:
        - Time to timeout for HTTP requests.
        type: int
        default: 30
    validate_certs:
        description:
        - Whether to validate HTTP certificates.
        type: bool
        default: yes
    org_name:
        description:
        - Name of organization.
        type: str
        aliases: [ organization ]
    org_id:
        description:
        - ID of organization.
        type: str
    rate_limit_retry_time:
        description:
        - Number of seconds to retry if rate limiter is triggered.
        type: int
        default: 165
    internal_error_retry_time:
        description:
        - Number of seconds to retry if server returns an internal server error.
        type: int
        default: 60
'''
