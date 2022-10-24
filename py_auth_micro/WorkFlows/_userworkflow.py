from dataclasses import dataclass
from tortoise.exceptions import DoesNotExist
import bcrypt
import re

from ..Models import User
from ..Exceptions import AlreadyExists
from ..Config import LDAPConfig, TokenConfig, AppConfig


@dataclass
class UserWorkflow:
    ldap_cfg: LDAPConfig
    token_cfg: TokenConfig
    app_cfg: AppConfig

    async def create_user(
        self,username: str, password: str, email: str, activated: bool = False
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
        
        #check Regexes
        if re.fullmatch(self.app_cfg.password_regex,password) is None:
            raise ValueError("bad password")
        if re.fullmatch(self.app_cfg.email_regex,email) is None:
            raise ValueError("bad email")
        if re.fullmatch(self.app_cfg.username_regex,username) is None:
            raise ValueError("bad username")

        # create password hash
        pw_salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)

        # now we can actualy create the user
        usr = await User.create(
            username=username, email=email, activated=activated, password_hash=pw_hash
        )
        return usr

    async def delete_user(access_token:str, username: str) -> bool:
        
        user = await User.get(username=username)
        await user.delete()
        return True

    async def change_user(username: str, **kwargs) -> User:
        user: User = await User.get(username=username)

        for key, value in kwargs.items():
            if key == "password":
                pw_salt = bcrypt.gensalt()
                value = bcrypt.hashpw(value.encode("utf-8"), pw_salt)
            setattr(user, key, value)
