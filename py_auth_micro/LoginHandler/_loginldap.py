try:
    import ldap
except ImportError:
    pass
import logging

from ._loginbaseclass import LoginBaseClass
from ..Config import LDAPConfig
from ..Core import LDAPHelper
from ..Models import User, Group


class LoginLDAP(LoginBaseClass):
    """Login Provider for LDAP/AD Users

    Keyword Arguments:
        ldap_config (LDAPConfig): configuration which are important for interacting with the LDAP.
        username (str): Username we want to authenticate.
        password (str): password for that specified user.
        user (User): Database instance of that user.
    """

    ldap_config: LDAPConfig
    username: str
    password: str
    user: User = None

    async def login(self) -> bool:
        """Checks User Credentials against the LDAP/AD.

        Note:
            calls :code:`self._sync_groups` to sync the LDAP/AD Group memberships of the User with the Database.

        Returns:
            bool: Successfull Login
        """
        logger = logging.getLogger(__name__)
        logger.debug(f"tyring to login {self.username} via LDAP")

        try:
            ldaphelper = LDAPHelper(self.ldap_config, self.username, self.password)
        except ldap.INVALID_CREDENTIALS:
            logger.debug(f"invalid credentials for {self.username}")
            return False

        if ldaphelper.login():
            await self._sync_groups(ldaphelper)
            return True
        logger.debug(f"User '{self.username}' is not allowed to log in via LDAP")
        return False

    async def _sync_groups(self, ldap_helper: LDAPHelper) -> None:
        """Syncs the Users Groups from LDAP to the Database.

        It will create non existing Groups and add the User to them.
        It will also remove the User from groups he is no part of anymore.

        Args:
            ldap_helper (LDAPHelper): LDAPHelper class instance to interact with the ldap
        """
        logger = logging.getLogger(__name__)
        logger.debug(f"syncing groups with LDAP for {self.username}")
        ldap_groups = ldap_helper.get_groups()
        db_groups = await self.user.groups.all().values_list("name", flat=True)

        add_groups = [
            added_group for added_group in ldap_groups if added_group not in db_groups
        ]
        rm_groups = [
            removed_group
            for removed_group in db_groups
            if removed_group not in ldap_groups
        ]

        logger.debug(f"User '{self.username}' will get removed from {rm_groups}")
        logger.debug(f"User '{self.username}' will be added to {add_groups}")

        # add user to group he should be in
        for add_group in add_groups:
            tmpgr, _ = await Group.get_or_create({"name": add_group}, name=add_group)
            await self.user.groups.add(tmpgr)

        # remove user from group he is not a member of anymore
        for rm_group in rm_groups:
            tmp_gr = await Group.get(name=rm_group)
            await self.user.groups.remove(tmp_gr)

        logger.debug(f"synced groups for User '{self.username}'")
