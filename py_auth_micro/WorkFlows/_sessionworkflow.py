from jwt_helper import JWTEncoder, JWTValidator

from ..LoginHandler import LoginHandler

from ..Models import User, Token
from ..Config import AppConfig, LDAPConfig


class SessionWorkflow:
    ldap_cfg: LDAPConfig
    jwt_encoder: JWTEncoder
    jwt_validator: JWTValidator
    app_cfg: AppConfig

    async def login(
        self, username: str, password: str, vhost: str = "test", ip: str = "*"
    ) -> str:
        user: User = await LoginHandler(username, password, self.ldap_cfg)
        return await user.create_id_token(self.jwt_encoder, self.app_cfg, vhost, ip)

    async def logout(self, id_token: str, ip: str = "*") -> bool:
        token = await Token.verify_id_jwt(self.jwt_validator,id_token,ip)
        user:User = await token.user

        return await user.revoke_id_token()

    async def get_access_token(self, id_token: str,ip:str) -> str:
        token = await Token.verify_id_jwt(self.jwt_validator,id_token,ip)
        access_jwt = await token.create_access_jwt(self.jwt_encoder,self.app_cfg)

        return access_jwt
