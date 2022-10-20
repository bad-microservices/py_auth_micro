from ..Config import TokenConfig
from ..Models import Token,User
from datetime import datetime


class JWTFunctions:
    token_config:TokenConfig

    def validate_token(self,to_verify:str,tokeninfo:Token) -> bool:

        raise NotImplementedError

    def create_token(self,user:User):

        raise NotImplementedError
    