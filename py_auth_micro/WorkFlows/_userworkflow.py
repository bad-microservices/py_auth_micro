import bcrypt
import re

from dataclasses import dataclass
from tortoise.exceptions import DoesNotExist
from jwt_helper import JWTEncoder, JWTValidator

from ..Models import User
from ..Exceptions import AlreadyExists, PermissionError
from ..Config import AppConfig


@dataclass
class UserWorkflow:
    jwt_encoder: JWTEncoder
    jwt_validator: JWTValidator
    app_cfg: AppConfig

    async def _create_user(
        self, username: str, password: str, email: str, activated: bool = False
    ) -> User:

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
        usr = await User.create(
            username=username, email=email, activated=activated, password_hash=pw_hash
        )
        return usr

    async def register_user(
        self,
        username: str,
        password: str,
        password_confirm: str,
        email: str,
        activated: bool = False,
    ) -> User:

        if password != password_confirm:
            raise ValueError("passwords do not match")

        return await self._create_user(
            username, password, email, self.app_cfg.auto_activate_accounts
        )

    async def admin_create_user(
        self, username: str, password: str, email: str, access_token
    ) -> User:
        _, is_admin = self._get_user_info(access_token)

        if not is_admin:
            raise PermissionError("Missing Permissions")

        return await self._create_user(username, password, email, True)

    async def delete_user(self, access_token: str, username: str) -> bool:

        user, is_admin = self._get_user_info(access_token)

        if not (is_admin or username == user):
            raise PermissionError("Not Authorized")

        user = await User.get(username=username)
        await user.delete()
        return True

    async def change_user(self, username: str, **kwargs) -> User:
        user: User = await User.get(username=username)

        for key, value in kwargs.items():
            if key == "password":
                pw_salt = bcrypt.gensalt()
                value = bcrypt.hashpw(value.encode("utf-8"), pw_salt)
            setattr(user, key, value)

    def _get_user_info(self, token: str) -> tuple[str, bool]:
        jwt_content = self.jwt_validator.get_jwt_as_dict(token)

        header: dict = jwt_content["headers"]
        user = jwt_content["payload"]["user"]

        is_admin = self.app_cfg.admin_group in header.get("aud", None)

        # TODO: implement

        raise NotImplementedError("finish this pls")
        # return user, is_admin
