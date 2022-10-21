import ldap

from ._loginbaseclass import LoginBaseClass
from ..Config import LDAPConfig
from ..Core import LDAPHelper
from ..Models import User, Group


class LoginLDAP(LoginBaseClass):
    ldap_config: LDAPConfig
    username: str
    password: str
    user: User = None
    
    async def login(self) -> bool:
        try:
            ldaphelper = LDAPHelper(self.ldap_config,self.username,self.password)
        except ldap.INVALID_CREDENTIALS:
            return False

        if ldaphelper.login():
            await self._sync_groups(ldaphelper)
            return True
        return False

    async def _sync_groups(self,ldap_helper:LDAPHelper) -> None:

        ldap_groups = ldap_helper.get_groups()
        db_groups = await self.user.groups.all().values_list("name", flat=True)

        add_groups = [added_group for added_group in ldap_groups if added_group not in db_groups] 
        rm_groups = [removed_group for removed_group in db_groups if removed_group not in ldap_groups]

        #add user to group he should be in
        for add_group in add_groups:  
            tmpgr, created = await Group.get_or_create({"name":add_group},name=add_group)
            await self.user.groups.add(tmpgr)

        #remove user from group he is not a member of anymore
        for rm_group in rm_groups:
            tmp_gr = await Group.get(name=rm_group)
            await self.user.groups.remove(tmp_gr)

        
