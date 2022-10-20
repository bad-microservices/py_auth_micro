from tortoise import fields
from tortoise.models import Model
from typing import Union
import jwt

import datetime

from ..Core import SignMethod
from ..Config import TokenConfig
from ._user import User


class Token(Model):
    """Databse Entity Holding Information around issued Identity Tokens

    This Entity holds Information about issued Tokens. The Token ID is supplied in the JWT Header.
    A User can only have one valid Identity Token Per Time. A Token is bound to a vhost for the Message Broker.
    The Vhost is not specified in the Identity Token and only gets supplied in the Access Token.

    Args:
        Model (_type_): _description_
    """

    user: fields.ManyToManyRelation["User"] = fields.ForeignKeyField(
        "models.User",
        related_name="token",
        pk=True,
        description="The User which relates to this Token",
    )
    token_id: int = fields.BigIntField(
        max_length=200, unique=True, description="ID of the Issued Token", index=True
    )
    ip: str = fields.CharField(
        max_length=39, description="IP That is valid for this User"
    )
    valid_until: datetime.datetime = fields.DatetimeField(
        auto_now_add=True,
        description="To what Time is this Token Valid",
        allows_generated=True,
        GENERATED_SQL="NOW()",
    )
    last_use: datetime.datetime = fields.DatetimeField(
        auto_now=True, description="Last Access Token creation time", null=True
    )
    sign_method: SignMethod = fields.CharEnumField(
        SignMethod,
        max_length=10,
        description="""Which Method got used to sign this Token
Valid Options>
 - HS256
 - HS384
 - HS512
 - RS256
 - RS384
 - RS512""",
    )
    vhost: str = fields.CharField(
        max_length=100, default="test", description="The Vhost for this Token"
    )

    async def get_id_jwt(self, token_config: TokenConfig):

        usergroups = []
        for group in self.user.groups:
            usergroups.append(str(group))

        return jwt.encode(
            {"groups": usergroups, "ip": self.ip},
            token_config.encode_secret(self.sign_method),
            headers={
                "kid": self.token_id,
                "iss": token_config.issuer,
                "iat": datetime.datetime.now(),
                "exp": self.valid_until,
            },
            algorithm=self.sign_method.value,
        )

    @staticmethod
    async def verify_id_jwt(
        token_config: TokenConfig,
        id_jwt: str,
        ip: Union[None, str] = None,
        ignore_issuer_mismatch: bool = False,
    ) -> "Token":

        # read header before verifying it
        token_header = jwt.get_unverified_header(id_jwt)

        # get token with matching token id from DB so we can compare...
        token = await Token.get(token_id=token_header["kid"])

        # get used sign method from DB
        alg = token.sign_method.value

        #verify send id jwt




        raise NotImplementedError

    async def create_access_jwt(self, token_config: TokenConfig) -> str:
        """Creates an Access JWT

        It's expected that you verify the ID JWT beforehand with `Token.verify_token()`

        Args:
            token_config (TokenConfig): Config to use for creating a Token

        Returns:
            str: _description_
        """
        raise NotImplementedError
