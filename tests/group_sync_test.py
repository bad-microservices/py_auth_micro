import pytest
from py_auth_micro.Models import Group, User


@pytest.mark.asyncio
class TestGroupWorkflow:

    async def test_create_group(self, initialize_tests):
        # This is from the LoginLDAP class

        user = await User.create(
            username="TestUser", email="test@test.test", activated=True
        )

        add_groups = ["does_not_exist_1", "does not exist as well"]

        for add_group in add_groups:
            tmpgr = await Group.get_or_none(name=add_group)
            if tmpgr is None:
                tmpgr = await Group.create(name=add_group)
            await user.groups.add(tmpgr)
        pass
