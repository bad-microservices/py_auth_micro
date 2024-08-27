import pytest


@pytest.mark.asyncio
class TestGroupWorkflow:

    async def test_create_group(
        self, initialize_tests, groupworkflow, access_token_admin
    ):
        resp = await groupworkflow.create_group(
            access_token=access_token_admin, groupname="Test2"
        )
        assert resp["resp_code"] == 200

    async def test_create_group_invalid_group(
        self, initialize_tests, groupworkflow, access_token_admin
    ):
        resp = await groupworkflow.create_group(
            access_token=access_token_admin, groupname="testasdasdasd asdasd____ asdasd"
        )
        assert resp["resp_code"] == 500

    async def test_create_group_double(
        self, initialize_tests, groupworkflow, access_token_admin
    ):
        with pytest.raises(ValueError):
            await groupworkflow.create_group(
                access_token=access_token_admin, groupname="test"
            )
            await groupworkflow.create_group(
                access_token=access_token_admin, groupname="test"
            )

    async def test_create_group_double_capitalisation(
        self, initialize_tests, groupworkflow, access_token_admin
    ):
        await groupworkflow.create_group(
            access_token=access_token_admin, groupname="test"
        )
        resp = await groupworkflow.create_group(
            access_token=access_token_admin, groupname="Test"
        )
        assert resp["resp_code"] == 200

    async def test_get_groups_empty(
        self, initialize_tests, groupworkflow, access_token_non_admin
    ):
        # print(str(await GROUPWORKFLOW.get_groups(access_token=blub)))
        resp = await groupworkflow.get_groups(access_token=access_token_non_admin)
        assert resp["resp_code"] == 204
        assert resp["resp_data"]["groups"] == []

    async def test_get_groups(self, test_data, groupworkflow, access_token_non_admin):
        print(groupworkflow)
        resp = await groupworkflow.get_groups(access_token=access_token_non_admin)
        assert resp["resp_code"] == 200
        assert resp["resp_data"]["groups"] == ["Test", "Test2"]
