import pytest
from plugins.modules.meraki_admin import find_admin


def test_find_admin_success():
    data = [
        {
            "id": "1234",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "authenticationMethod": "Email",
            "orgAccess": "full",
            "accountStatus": "ok",
            "twoFactorAuthEnabled": True,
            "hasApiKey": False,
            "lastActive": "2022-04-13T13:48:51Z",
            "networks": [],
            "tags": [],
        },
        {
            "id": "4321",
            "name": "Jane Doe",
            "email": "jane.dow@example.com",
            "authenticationMethod": "Email",
            "orgAccess": "full",
            "accountStatus": "ok",
            "twoFactorAuthEnabled": False,
            "hasApiKey": False,
            "lastActive": "2021-05-13T18:58:32Z",
            "networks": [],
            "tags": [],
        },
    ]
    result = find_admin(data, "john.doe@example.com")
    assert result == data[0]


def test_find_admin_fail():
    data = [
        {
            "id": "1234",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "authenticationMethod": "Email",
            "orgAccess": "full",
            "accountStatus": "ok",
            "twoFactorAuthEnabled": True,
            "hasApiKey": False,
            "lastActive": "2022-04-13T13:48:51Z",
            "networks": [],
            "tags": [],
        },
        {
            "id": "4321",
            "name": "Jane Doe",
            "email": "jane.dow@example.com",
            "authenticationMethod": "Email",
            "orgAccess": "full",
            "accountStatus": "ok",
            "twoFactorAuthEnabled": False,
            "hasApiKey": False,
            "lastActive": "2021-05-13T18:58:32Z",
            "networks": [],
            "tags": [],
        },
    ]
    result = find_admin(data, "not.john.doe@example.com")
    assert result == None
