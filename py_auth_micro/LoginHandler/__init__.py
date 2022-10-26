"""The :code:`LoginHandler` Package contains classes for different identity Sources.

Currently there are Classes to work with the following identity Sources:

    * :code:`LoginLocal` - for a Local Database
    * :code:`LoginLDAP` - for LDAP
    * :code:`LoginKerberos` - for Kerberos

These are choosen automatically by the :code:`auth_type` field connected to every Users DB Entry.
The :code:`auth_type` is an :code:`AuthSource`.

"""
import logging

from tortoise.exceptions import DoesNotExist
from typing import Optional

from ._loginbaseclass import LoginBaseClass
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



async def login(
    username: str, password: str, ldap_config: Optional[LDAPConfig] = None
) -> User:
    """Function which logs a user in with specified Credentials.

    Args:
        username (str): Username of the User
        password (str): Password of the User
        ldap_config (LDAPConfig, optional): Configuration for LDAPAuth. Defaults to None.

    Raises:
        ValueError: If the Credentials are wrong

    Returns:
        User: the User mathcing the credentials
    """
    logger = logging.getLogger(__name__)

    logger.info(f"Login attempt for {username}")

    possible_user = await _get_user_from_db(username, password, ldap_config)

    logger.debug(f"User '{username}' exists in DB")

    logger.debug(f"AuthType is {possible_user.auth_type}")
    login_handler = LOGINHANDLER[possible_user.auth_type](
        user=possible_user,
        ldap_config=ldap_config,
        username=username,
        password=password,
    )
    if not await login_handler.login():
        logger.debug(f"Could not log in User '{username}'!")
        raise ValueError("could not log in")
    logger.info(f"User '{username}' successfully logged in.")
    return login_handler.user


async def _get_user_from_db(
    username: str, password: str, ldap_config: Optional[LDAPConfig] = None
) -> User:
    logger = logging.getLogger(__name__)
    try:
        logger.debug(f"trying to get User '{username}' from DB")
        user = await User.get(username=username)
        return user

    except DoesNotExist as exc:
        logger.info(f"user '{username}' does not exist in DB")
        # try LDAP
        try:
            logger.debug(f"try to auth user '{username}' with ldap")
            helper = LDAPHelper(ldap_config, username, password)
            # if the user can be authenticated with ldap create him in the DB
            if helper.login():
                logger.debug(f"User '{username}' could auth with the LDAP -> creating DB Entry")
                user = await User.create(
                    username=username,
                    password_hash=None,
                    activated=True,
                    auth_type=AuthSource.LDAP,
                    email=helper.email,
                )
                return user
        except Exception:
            logger.debug(f"user '{username}' could not auth with LDAP")
            raise DoesNotExist

        # if the user cant log in with ldap reraise the exc
        raise exc


__all__ = ["login", "LoginBaseClass", "LoginLDAP", "LoginLocal", "LoginKerberos"]
