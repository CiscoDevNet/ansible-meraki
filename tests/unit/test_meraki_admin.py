import pytest
from plugins.modules.meraki_admin import find_admin, get_admin_id


@pytest.fixture
def admin_data():
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
    return data


def test_find_admin_success(admin_data):
    result = find_admin(admin_data, "john.doe@example.com")
    assert result == admin_data[0]


def test_find_admin_fail(admin_data):
    result = find_admin(admin_data, "not.john.doe@example.com")
    assert result == None


def test_get_admin_id_by_name_success(admin_data):
    result = get_admin_id(
        {"name": "John Doe", "id": "1234"}, admin_data, name="John Doe"
    )
    assert result[0] == admin_data[0]["id"]


def test_get_admin_id_by_namenot_found(admin_data):
    result = get_admin_id(
        {"name": "Not John Doe", "id": "1234"}, admin_data, name="ASDF"
    )
    assert result[1] == "No admin_id found"


def test_get_admin_id_by_email_success(admin_data):
    result = get_admin_id(
        {"name": "John Doe", "id": "1234"}, admin_data, email="john.doe@example.com"
    )
    assert result[0] == admin_data[0]["id"]


def test_get_admin_id_by_emailnot_found(admin_data):
    result = get_admin_id(
        {"name": "Not John Doe", "id": "1234"},
        admin_data,
        email="not.john.doe@example.com",
    )
    assert result[1] == "No admin_id found"
