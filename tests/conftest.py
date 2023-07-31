import pytest
import asyncio
import pytest_asyncio

from tortoise import Tortoise
from tortoise.contrib.test import getDBConfig
from jwt_helper import JWTValidator, Issuer, SignMethod, JWTEncoder

from py_auth_micro.Config import AppConfig
from py_auth_micro.WorkFlows import GroupWorkflow

DBURL = "sqlite://db.sqlite3"


@pytest.fixture
def initialize_tests(request):
    config = getDBConfig(app_label="models", modules=["py_auth_micro.Models"])
    loop = asyncio.get_event_loop()

    async def _init_db() -> None:
        await Tortoise.init(config)
        await Tortoise.generate_schemas(safe=False)

    async def _close_db() -> None:
        await Tortoise.close_connections()

    loop.run_until_complete(_init_db())

    request.addfinalizer(lambda: loop.run_until_complete(_close_db()))


@pytest.fixture
def encoder():
    return JWTEncoder("test_issuer", SignMethod.HS256, "123123")


@pytest.fixture
def access_token_admin(encoder):
    return encoder.create_jwt(
        {
            "aud": ["test", "admin"],
            "Type": "Access-Token",
            "vhost": "test",
        },
        {"user": "test"},
        3600,
    )


@pytest.fixture
def access_token_non_admin(encoder):
    return encoder.create_jwt(
        {
            "aud": ["test", "not_admin"],
            "Type": "Access-Token",
            "vhost": "test",
        },
        {"user": "test"},
        3600,
    )


@pytest.fixture
def id_token(encoder):
    return encoder.create_jwt(
        {
            "kid": "1",
            "aud": "127.0.0.1",
            "vhost": "test",
            "type": "ID-Token",
        },
        {"groups": ["test", "admin"], "username": "testuser"},
        3600,
    )


@pytest_asyncio.fixture
async def groupworkflow(initialize_tests):
    return GroupWorkflow(
        JWTValidator(
            {"test_issuer": Issuer("test_issuer", "123123", [SignMethod.HS256])}
        ),
        AppConfig(),
    )


@pytest_asyncio.fixture
async def test_data(initialize_tests, groupworkflow, access_token_admin):
    await groupworkflow.create_group(access_token=access_token_admin, groupname="Test")
    await groupworkflow.create_group(access_token=access_token_admin, groupname="Test2")
