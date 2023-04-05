from jwt_helper import JWTEncoder, JWTValidator
from dataclasses import dataclass
from typing import Optional

from ..LoginHandler import login
from ..Models import User, Token
from ..Config import AppConfig, LDAPConfig


@dataclass
class SessionWorkflow:
    """This Helper Class contains all interactions related to Sessions.

    Attributes:
        ldap_cfg (LDAPConfig): Configuration regarding the LDAP connection.
        jwt_encoder (JWTEncoder): JWTEncoder used to create Tokens.
        jwt_validator (JWTValidator): JWTValidator used to check Tokens with.
        app_cfg (AppConfig): Some miscellaneous settings regarding the Application.
    """

    ldap_cfg: LDAPConfig
    jwt_encoder: JWTEncoder
    jwt_validator: JWTValidator
    app_cfg: AppConfig

    async def login(
        self,
        *,
        username: str,
        password: str,
        vhost: Optional[str] = None,
        ip: str = "*",
        **kwargs
    ) -> dict:
        """This Function checks the User Credentials and returns an ID-Token on success.

        Args:
            username (str): Username of the User.
            password (str): Password of the User.
            vhost (str, optional): VHost for which the ID-Token is valid. Defaults to "test".
            ip (str, optional): IP of the Host making the Request. The ID-Token gets bound to that Request-IP. Defaults to "*".

        Returns:
            dict: `resp_data` contains the id_token
        """

        if vhost is None:
            vhost = self.app_cfg.default_vhost
            
        user: User = await login(username, password, self.ldap_cfg)
        token_obj = await user.create_id_token(
            self.jwt_encoder, self.app_cfg, vhost, ip
        )
        return {
            "resp_code": 200,
            "resp_data": {
                "id_token": await token_obj.get_id_jwt(self.jwt_encoder, self.app_cfg)
            },
        }

    async def logout(self, *, id_token: str, ip: str = "*", **kwargs) -> dict:
        """Invalidates the ID-Token given and thereby logs the User out

        Args:
            id_token (str): The ID-Token as JWT
            ip (str, optional): IP Address making the Request. Used for validating the ID-Token. Defaults to "*".

        Returns:
            dict: `resp_code` = 200 if logout was successfull, `resp_code` = 500 if it was not
        """
        token = await Token.verify_id_jwt(self.jwt_validator, id_token, ip)
        user: User = await token.user

        success = await user.revoke_id_token()

        if success:
            return {"resp_code": 200, "resp_data": {"msg": "Logout was successfull"}}

        return {"resp_code": 500, "resp_data": {"msg": "Logout was not successfull"}}

    async def get_access_token(self, *, id_token: str, ip: str = "*", **kwargs) -> str:
        """Verifies an ID-Token and returns an Access-Token

        Args:
            id_token (str): The ID-Token of the Requesting User
            ip (str, optional): IP-Address of the requesting User. Defaults to "*".

        Returns:
            dict: `resp_data` contains `access_token`
        """
        token = await Token.verify_id_jwt(self.jwt_validator, id_token, ip)
        access_jwt = await token.create_access_jwt(self.jwt_encoder, self.app_cfg)

        return {"resp_code": 200, "resp_data": {"access_token": access_jwt}}
