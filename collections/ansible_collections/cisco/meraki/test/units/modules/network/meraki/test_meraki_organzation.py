# -*- coding: utf-8 -*-

# Copyright 2019 Kevin Breit <kevin.breit@kevinbreit.net>

# This file is part of Ansible by Red Hat
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os
import pytest

from units.compat import unittest, mock
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.meraki.meraki import MerakiModule, meraki_argument_spec
from ansible.module_utils.six import PY2, PY3
from ansible.module_utils._text import to_native, to_bytes
from ansible.modules.network.meraki.meraki_organization
from units.modules.utils import set_module_args

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}
testcase_data = {
    "params": {'orgs': ['orgs.json'],
               }
}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    # try:
    data = json.loads(data)
    # except Exception:
    #     pass

    fixture_data[path] = data
    return data


# @pytest.fixture(scope="module")
# def meraki():
#     # argument_spec = meraki_argument_spec()
#     set_module_args({'auth_key': 'abc123',
#                      'org_name': 'test_org',
#                      'state': 'absent',
#                      })
#     module = AnsibleModule(argument_spec=argument_spec,
#                            supports_check_mode=False)
#     meraki = MerakiModule(module, function='organization')
#     return MerakiModule(meraki)


# def test_fetch_url_404(module, mocker):
#     url = '404'
#     mocker.patch('ansible.module_utils.network.meraki.meraki.fetch_url', side_effect=mocked_fetch_url)
#     mocker.patch('ansible.module_utils.network.meraki.meraki.MerakiModule.fail_json', side_effect=mocked_fail_json)
#     with pytest.raises(HTTPError):
#         data = module.request(url, method='GET')
#     assert module.status == 404


def test_org_delete_no_confirmation(mocker):
    mocker.patch(meraki_organization)
    org_response = meraki_organization()
    print(org_response)
