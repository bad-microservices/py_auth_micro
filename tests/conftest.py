import pytest
from tortoise.contrib.test import finalizer, initializer


DBURL="sqlite://db.sqlite3"


@pytest.fixture(autouse=True)
def initialize_tests(request):
    initializer(["py_auth_micro.Models"], db_url=DBURL, app_label="models")
    request.addfinalizer(finalizer)