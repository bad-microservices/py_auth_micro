from dataclasses import dataclass
from tortoise.exceptions import DoesNotExist

from typing import Optional

from ._loginldap import LoginLDAP
from ._loginkerberos import LoginKerberos
from ._loginlocal import LoginLocal

from ..Config import LDAPConfig
from ..Models import User

from ..Core import LDAPHelper, AuthSource

LOGINHANDLER = {
    AuthSource.LDAP: LoginLDAP,
    AuthSource.LOCAL: LoginLocal,
    AuthSource.KERBEROS: LoginKerberos,
}


class LoginHandler:
    async def __new__(
        self, username: str, password: str, ldap_config: Optional[LDAPConfig] = None
    ) -> User:

        possible_user = await self._get_login_type(username, password, ldap_config)

        login_handler = LOGINHANDLER[possible_user.auth_type](
            user=possible_user,
            ldap_config=ldap_config,
            username=username,
            password=password,
        )
        if not await login_handler.login():
            raise ValueError("could not log in")

        return login_handler.user

    async def _get_login_type(
        username: str, password: str, ldap_config: Optional[LDAPConfig] = None
    ) -> User:
        try:
            user = await User.get(username=username)
            return user

        except DoesNotExist as exc:
            # try LDAP
            try:
                helper = LDAPHelper(ldap_config, username, password)
                # if the user can be authenticated with ldap create him in the DB
                if helper.login():
                    user = await User.create(
                        username=username,
                        password_hash=None,
                        activated=True,
                        auth_type=AuthSource.LDAP,
                        email=helper.email,
                    )
                    return user
            except Exception:
                raise DoesNotExist

            # if the user cant log in with ldap reraise the exc
            raise exc
