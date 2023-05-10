import pytest
import importlib
from pathlib import Path
import sys
from tortoise.contrib import test

MODULE_PATH = f"{Path(__file__).parents[1]}/py_auth_micro/__init__.py"
MODULE_NAME = "py_auth_micro"
spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

from py_auth_micro.Config import AppConfig
from py_auth_micro.WorkFlows import GroupWorkflow
from jwt_helper import JWTValidator, Issuer, SignMethod, JWTEncoder

GROUPWORKFLOW = GroupWorkflow(
    JWTValidator({"test_issuer": Issuer("test_issuer", "123123", [SignMethod.HS256])}),
    AppConfig(),
)
ENCODER = JWTEncoder("test_issuer", SignMethod.HS256, "123123")

ACCESS_TOKEN_ADMIN = ENCODER.create_jwt(
    {
        "aud": ["test", "admin"],
        "Type": "Access-Token",
        "vhost": "test",
    },
    {"user": "test"},
    3600,
)

ACCESS_TOKEN_NON_ADMIN = ENCODER.create_jwt(
    {
        "aud": ["test", "not_admin"],
        "Type": "Access-Token",
        "vhost": "test",
    },
    {"user": "test"},
    3600,
)

ID_TOKEN = ENCODER.create_jwt(
    {
        "kid": "1",
        "aud": "127.0.0.1",
        "vhost": "test",
        "type": "ID-Token",
    },
    {"groups": ["test", "admin"], "username": "testuser"},
    3600,
)


class TestGroupWorkflow(test.TestCase):
    @pytest.mark.asyncio
    async def test_create_group(self):
        resp = await GROUPWORKFLOW.create_group(
            access_token=ACCESS_TOKEN_ADMIN, groupname="Test2"
        )
        assert resp["resp_code"] == 200

    async def test_create_group_invalid_group(self):
        resp = await GROUPWORKFLOW.create_group(
            access_token=ACCESS_TOKEN_ADMIN, groupname="testasdasdasd asdasd____ asdasd"
        )
        assert resp["resp_code"] == 500

    async def test_create_group_double(self):
        with pytest.raises(ValueError):
            await GROUPWORKFLOW.create_group(
                access_token=ACCESS_TOKEN_ADMIN, groupname="test"
            )
            await GROUPWORKFLOW.create_group(
                access_token=ACCESS_TOKEN_ADMIN, groupname="test"
            )

    async def test_create_group_double_capitalisation(self):
        await GROUPWORKFLOW.create_group(
            access_token=ACCESS_TOKEN_ADMIN, groupname="test"
        )
        resp = await GROUPWORKFLOW.create_group(
            access_token=ACCESS_TOKEN_ADMIN, groupname="Test"
        )
        assert resp["resp_code"] == 200

    async def test_get_groups_empty(self):
        # print(str(await GROUPWORKFLOW.get_groups(access_token=blub)))
        resp = await GROUPWORKFLOW.get_groups(access_token=ACCESS_TOKEN_NON_ADMIN)
        assert resp["resp_code"] == 204
        assert resp["resp_data"]["groups"] == []

    async def test_get_groups(self):
        # print(str(await GROUPWORKFLOW.get_groups(access_token=blub)))
        await GROUPWORKFLOW.create_group(
            access_token=ACCESS_TOKEN_ADMIN, groupname="Test"
        )
        await GROUPWORKFLOW.create_group(
            access_token=ACCESS_TOKEN_ADMIN, groupname="Test2"
        )
        resp = await GROUPWORKFLOW.get_groups(access_token=ACCESS_TOKEN_NON_ADMIN)
        assert resp["resp_code"] == 200
        assert resp["resp_data"]["groups"] == ["Test","Test2"]
