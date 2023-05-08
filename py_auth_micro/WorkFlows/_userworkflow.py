import bcrypt
import re

from dataclasses import dataclass
from tortoise.exceptions import DoesNotExist
from jwt_helper import JWTValidator
from typing import Optional

from ..Models import User
from ..Exceptions import AlreadyExists
from ..Config import AppConfig
from ..Core import AuthSource

from ._misc import _get_info_from_token


@dataclass
class UserWorkflow:
    """This Helper Class contains all interactions related to Users.

    Attributes:
        jwt_validator (JWTValidator): JWTValidator used to check Tokens with.
        app_cfg (AppConfig): Some miscellaneous settings regarding the Application.
    """

    jwt_validator: JWTValidator
    app_cfg: AppConfig

    async def get_all(self, *, access_token: str, **kwargs) -> dict[str, list[str]]:
        """Returns a list of all Usernames.

        Args:
            access_token (str): Access Token of the Requesting User

        Raises:
            PermissionError: If the Access Token is invalid

        Returns:
            dict : A list of all known Users
        """
        if not self.jwt_validator.verify_jwt(access_token):
            raise PermissionError("Not Authorized")

        users = await User.all().values_list("username", flat=True)

        return {"resp_code": 200, "resp_data": {"users": users}}

    async def _create_user(
        self,
        *,
        username: str,
        password: str,
        email: str,
        activated: bool = False,
        **kwargs,
    ) -> bool:
        """Creates a Local User with the specified Values.

        Args:
            username (str): Username.
            password (str): Password of the User.
            email (str): email address of the User.
            activated (bool, optional): Is the User activated?. Defaults to False.

        Raises:
            AlreadyExists: If the username or email address are already taken
            ValueError: If a Value does not match the specified Regexes in the AppConfig

        Returns:
            bool: True -> User created successfully
        """

        # check if username or email is already taken
        try:
            await User.get(username=username)
            raise AlreadyExists("username already Taken")
        except DoesNotExist:
            pass

        try:
            await User.get(email=email)
            raise AlreadyExists("email is already Taken")
        except DoesNotExist:
            pass

        # check Regexes
        if re.fullmatch(self.app_cfg.password_regex, password) is None:
            raise ValueError("bad password")
        if re.fullmatch(self.app_cfg.email_regex, email) is None:
            raise ValueError("bad email")
        if re.fullmatch(self.app_cfg.username_regex, username) is None:
            raise ValueError("bad username")

        # create password hash
        pw_salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)

        # now we can actualy create the user
        await User.create(
            username=username, email=email, activated=activated, password_hash=pw_hash
        )
        return True

    async def register_user(
        self,
        *,
        username: str,
        password: str,
        password_confirm: str,
        email: str,
        **kwargs,
    ) -> dict:
        """This Function is for User Registration

        Args:
            username (str): Username.
            password (str): Password of the User
            password_confirm (str): Confirmation of the Password
            email (str): Email Address of the User

        Raises:
            ValueError: some Values do not match the specified Regexes or the password confirmation does not match the Password.

        Returns:
            dict: `resp_code` 200 if operation was successfull
        """

        if password != password_confirm:
            raise ValueError("passwords do not match")

        user_created = await self._create_user(
            username=username,
            password=password,
            email=email,
            activated=self.app_cfg.auto_activate_accounts,
        )

        if user_created:
            return {"resp_code": 201, "resp_data": {"msg": f"created user {username}"}}

        return {
            "resp_code": 400,
            "resp_data": {"msg": f"could not create user {username}"},
        }

    async def get_user(
        self, *, username: str, access_token: Optional[str] = None, **kwargs
    ) -> dict:
        """Returns a dictionary containing Userinformation.

        This Function returns more Information if you are the User you are requesting.
        Even more Info is provided if you are an Administrator

        Args:
            username (str): Username of the User we want the Data from
            access_token (str, optional): Access Token of the Requesting User. Defaults to None.

        Returns:
            dict: Dictionary containing User Information
        """
        try:
            user = await User.get(username=username)
        except Exception:
            return "wtf"

        user_dict = {}
        user_dict["username"] = user.username
        user_dict["activated"] = user.activated
        user_dict["created_at"] = user.created_at.isoformat()

        if access_token is None:
            return user_dict

        requesting_user, is_admin = _get_info_from_token(
            self.jwt_validator, self.app_cfg, access_token
        )

        if user.username != requesting_user and not is_admin:
            return user_dict

        token = await user.token

        if token is None:
            user_dict["token_info"] = None
            return user_dict

        user_dict["token_info"] = {
            "valid_until": token.valid_until.isoformat(),
            "last_use": token.last_use.isoformat(),
            "vhost": token.vhost,
        }

        if is_admin:
            user_dict["auth_type"] = user.auth_type.name
            user_dict["token_info"].update(
                {
                    "kid": token.token_id,
                    "ip": token.ip,
                    "sign_method": token.sign_method.value,
                }
            )

        return {"resp_code": 200, "resp_data": user_dict}

    async def admin_create_user(
        self, *, username: str, password: str, email: str, access_token: str, **kwargs
    ) -> dict:
        """Lets an administrator create an User

        Args:
            username (str): Username of the new User.
            password (str): Password of the new User.
            email (str): Email of the new User.
            access_token (str): Access Token of the Administrator

        Raises:
            PermissionError: If the User is not an administrator this gets raised

        Returns:
            dict: :code:`{"success":True}` if operation was successfull
        """
        _, is_admin = _get_info_from_token(
            self.jwt_validator, self.app_cfg, access_token
        )

        if not is_admin:
            raise PermissionError("Missing Permissions")

        created = await self._create_user(
            username=username, password=password, email=email, activated=True
        )

        if created:
            return {"resp_code": 201, "resp_data": {"msg": f"created user {username}"}}

        return {
            "resp_code": 400,
            "resp_data": {"msg": f"could not create user {username}"},
        }

    async def delete_user(self, *, access_token: str, username: str, **kwargs) -> dict:
        """A user can delete himself or an Administrator can do so as well

        Args:
            access_token (str): Token of the requesting user.
            username (str): username of the user to be deleted.

        Raises:
            PermissionError: If you are not an admin or the User itself

        Returns:
            dict: :code:`{"success":True}` if operation was successfull
        """

        user, is_admin = _get_info_from_token(
            self.jwt_validator, self.app_cfg, access_token
        )

        if not (is_admin or username == user):
            raise PermissionError("Not Authorized")

        user = await User.get(username=username)
        await user.delete()
        return {"resp_code": 200, "resp_data": {"msg": f"deleted user {username}"}}

    async def change_user(
        self,
        *,
        username: str,
        access_token: str,
        password: Optional[str] = None,
        email: Optional[str] = None,
        activated: Optional[bool] = None,
        **kwargs,
    ) -> dict:
        """Used to change a User

        For Ldap authenticated Users you ca only change the Activation state.
        The activation State can only be changed by an Administrator.

        Important:
            Changing the users password will invalidate that Users ID-Token!

        Args:
            username (str): username of the User we want to change Information for
            access_token (str): Token of the Requesting User.
            password (str, optional): New Password. Defaults to None.
            email (str, optional): new Email of the User. Defaults to None.
            activated (bool, optional): Activation State for the User. Defaults to None.

        Raises:
            PermissionError: Not Authorized to change Userinformation
            ValueError: Changed Value is invalid

        Returns:
            dict: :code:`{"success":True}` if operation was successfull
        """

        req_user, is_admin = _get_info_from_token(
            self.jwt_validator, self.app_cfg, access_token
        )

        # check if we are allowed to even change the user
        if req_user != username or not is_admin:
            raise PermissionError("Missing Permission")

        user: User = await User.get(username=username)

        # check if its an local user or an AD User
        is_ad_user = (
            user.auth_type == AuthSource.LDAP or user.auth_type == AuthSource.KERBEROS
        )

        if is_ad_user and (password is not None or email is not None):
            raise ValueError("can't change Attribute for AD User")

        if not is_admin and activated is not None:
            raise PermissionError("Unauthorized")

        if email is not None:
            # check email
            if re.fullmatch(self.app_cfg.email_regex, email) is None:
                raise ValueError("bad email")
            user.email = email

        if activated is not None:
            user.activated = activated

        if password is not None:
            # create password hash
            if re.fullmatch(self.app_cfg.password_regex, password) is None:
                raise ValueError("bad password")
            pw_salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)
            user.password_hash = pw_hash
            await user.revoke_id_token()

        await user.save()

        return {
            "resp_code": 200,
            "resp_data": {"msg": f"changed data for user {username}"},
        }
