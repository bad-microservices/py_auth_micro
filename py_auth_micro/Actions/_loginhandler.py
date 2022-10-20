from tortoise.exceptions import DoesNotExist

from ..Config import LDAPConfig
from ..Models import User,UserGroup,Token

from ..Core import LDAPHelper,AuthSource

class LoginHandler:
    ldap_config:LDAPConfig

    async def login(self,username:str,password:str):
        
        login_type = self._get_login_type(username,password)

    async def _get_login_type(self,username,password):

        try:
            user = await User.get(username=username)

            return user.auth_type
        
        except DoesNotExist:
            #try LDAP
            helper = LDAPHelper(self.ldap_config)
            # if the user can be authenticated with ldap create him in the DB
            if helper.login(username,password):
                User.create(username=username,password_hash=None,activated=True,auth_type=AuthSource.LDAP)
        