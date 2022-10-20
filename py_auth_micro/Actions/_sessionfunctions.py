from dataclasses import dataclass
from tortoise.exceptions import DoesNotExist

from ..Config import LDAPConfig
from ..Models import User, UserGroup, Token

from ..Core import LDAPHelper, AuthSource
from ..LoginHandler import LOGINHANDLER


@dataclass
class SessionFunctions:
    ldap_config: LDAPConfig

    async def login(self, username: str, password: str) -> bool:

        # get the Authorisation Source for the specified User
        login_type = await self._get_login_type(username, password)

        # perform the actual Login!
        successful_login = LOGINHANDLER[login_type](
            ldap_config=self.ldap_config, username=username, password=password
        )

        return successful_login

    async def _get_login_type(self, username: str, password: str) -> AuthSource:
        try:
            user = await User.get(username=username)
            return user.auth_type

        except DoesNotExist as exc:
            # try LDAP
            helper = LDAPHelper(self.ldap_config)
            # if the user can be authenticated with ldap create him in the DB
            if helper.login(username, password):
                await User.create(
                    username=username,
                    password_hash=None,
                    activated=True,
                    auth_type=AuthSource.LDAP,
                )
                return AuthSource.LDAP
            # if the user cant log in with ldap reraise the exc
            raise exc
