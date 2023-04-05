from jwt_helper import JWTValidator
from dataclasses import dataclass
from typing import Optional

from ..Models import Group, User
from ..Config import AppConfig

from ._misc import _get_info_from_token


@dataclass
class GroupWorkflow:
    """This Helper Class contains all interactions related to Groups and Group Memberships.

    Attributes:
        jwt_validator (JWTValidator): JWTValidator used to check Tokens with.
        app_cfg (AppConfig): Some miscellaneous settings regarding the Application.
    """

    jwt_validator: JWTValidator
    app_cfg: AppConfig

    async def _perm_and_name_check(
        self, *, access_token: str, group_name: str, **kwargs
    ) -> Optional[Group]:
        """Will check the Permissions of the access Token and if the group already exists.

        Args:
            access_token (str): Access Token of the Request Sender.
            group_name (str): Name of the Group to check for

        Raises:
            PermissionError: User Requesting the Action is not and Administrator.

        Returns:
            Optional[Group]: If the Group exists return it. None if it does not exist.
        """
        _, is_admin = _get_info_from_token(
            self.jwt_validator, self.app_cfg, access_token
        )

        if not is_admin:
            raise PermissionError("Not Authorized")

        group = await Group.get_or_none(name=group_name)

        if group is None:
            return None

        return group

    async def get_groups(self, *, access_token: str, **kwargs) -> dict:
        """This Function returns a list of all Groups

        Args:
            access_token (str): Access-Token of the Requesting User.

        Returns:
            dict: `resp_data` contains the key groups which is a list of all groups.
        """
        self.jwt_validator.verify_jwt(access_token)
        groups_raw = await Group.all()

        groups = []

        for group in groups_raw:
            groups.append(group.name)

        if len(groups) == 0:
            status_code = 204
        else:
            status_code = 200

        return {"resp_code": status_code, "resp_data": {"groups": groups}}

    async def create_group(
        self, *, access_token: str, group_name: str, **kwargs
    ) -> dict:
        """Creates a Group with the specified Name

        Args:
            access_token (str): Access-Token of the Requesting User.
            group_name (str): Name of the Group to create.

        Raises:
            ValueError: Group already exists.

        Returns:
            dict: `resp_code` = 200 action was successfull, `resp_code` = 500 if it was not
        """
        # check groups Existence and Requesting Users Permission
        if await self._perm_and_name_check(access_token, group_name) is not None:
            raise ValueError("Group already exist")

        try:
            await Group.create(name=group_name)
        except Exception:
            return {
                "resp_code": 500,
                "resp_data": {"msg": f"could not create group {group_name}"},
            }

        return {"resp_code": 200, "resp_data": {"msg": f"created group {group_name}"}}

    async def delete_group(
        self, *, access_token: str, group_name: str, **kwargs
    ) -> dict:
        """Deletes the specified Group.

        Args:
            access_token (str): Access-Token of the Requesting User.
            group_name (str): Name of the Group to delete.

        Raises:
            ValueError: Group does not exist

        Returns:
            dict: `resp_code` = 200 action was successfull, `resp_code` = 500 if it was not
        """
        # check groups Existence and Requesting Users Permission
        group = await self._perm_and_name_check(access_token, group_name)

        if group is None:
            raise ValueError("Group does not exist")

        try:
            await group.delete()
        except Exception:
            return {
                "resp_code": 500,
                "resp_data": {"msg": f"could not delete group {group_name}"},
            }

        return {"resp_code": 200, "resp_data": {"msg": f"deleted group {group_name}"}}

    async def add_user_to_group(
        self, *, access_token: str, group_name: str, user_name: str, **kwargs
    ) -> dict:
        """Adds a User to a group

        Args:
            access_token (str): Access Token of the Requesting User.
            group_name (str): Name of the Group to add the User to.
            user_name (str): Name of the User to add to the Group.

        Raises:
            ValueError: Group does not exist.

        Returns:
            dict: `resp_code` = 200 action was successfull, `resp_code` = 500 if it was not
        """

        # check groups Existence and Requesting Users Permission
        group = await self._perm_and_name_check(access_token, group_name)

        if group is None:
            raise ValueError("Group does not exist")

        user = await User.get(username=user_name)

        try:
            await group.users.add(user)
        except Exception:
            return {
                "resp_code": 500,
                "resp_data": {
                    "msg": f"could not add user {user_name} to group {group_name}"
                },
            }

        return {
            "resp_code": 200,
            "resp_data": {"msg": f"added user {user_name} to group {group_name}"},
        }

    async def remove_user_from_group(
        self, *, access_token: str, group_name: str, user_name: str, **kwargs
    ) -> dict:
        """Removes a User from a group

        Args:
            access_token (str): Access Token of the Requesting User.
            group_name (str): Name of the Group to remove the User from.
            user_name (str): Name of the User to remove the Group.

        Raises:
            ValueError: Group does not exist.

        Returns:
            dict: `resp_code` = 200 action was successfull, `resp_code` = 500 if it was not
        """

        # check groups Existence and Requesting Users Permission
        group = await self._perm_and_name_check(access_token, group_name)

        if group is None:
            raise ValueError("Group does not exist")

        user = await User.get(username=user_name)

        try:
            await group.users.remove(user)
        except Exception:
            return {
                "resp_code": 500,
                "resp_data": {
                    "msg": f"could not remove user {user_name} to group {group_name}"
                },
            }

        return {
            "resp_code": 200,
            "resp_data": {"msg": f"removed user {user_name} to group {group_name}"},
        }
