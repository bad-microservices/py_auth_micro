from tortoise import fields
from tortoise.models import Model
from typing import Optional
import jwt
import datetime

from jwt_helper import SignMethod, JWTEncoder, JWTValidator

from ..Config import AppConfig

class Token(Model):
    """Databse Entity Holding Information around issued Identity Tokens

    This Entity holds Information about issued Tokens. The Token ID is supplied in the JWT Header.
    A User can only have one valid Identity Token Per Time. A Token is bound to a vhost for the Message Broker.
    The Vhost is not specified in the Identity Token and only gets supplied in the Access Token.

    Args:
        Model (_type_): _description_
    """

    user: fields.OneToOneRelation["User"] = fields.OneToOneField(
        "models.User",
        related_name="token",
        description="The User which relates to this Token",
    )
    token_id: int = fields.BigIntField(
        unique=True,
        description="ID of the Issued Token",
        pk=True,
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

    async def get_id_jwt(self, jwt_encoder: JWTEncoder,app_cfg: AppConfig) -> str:

        usergroups = await self.user.groups.all().values_list("name", flat=True)

        token = jwt_encoder.create_jwt({
                "kid": str(self.token_id),
                "aud": self.ip,
                "vhost": self.vhost,
                "type": "ID-Token",
            },{"groups": usergroups, "username": str(self.user)},app_cfg.id_token_valid_time)
        
        return token

    @staticmethod
    async def verify_id_jwt(
        jwt_validator: JWTValidator,
        id_jwt: str,
        ip: Optional[str] = None,
    ):

        if not jwt_validator.check_token(id_jwt):
            raise ValueError("invalid ID-JWT")

        

        if token_header["type"] != "ID-Token":
            raise ValueError("not an ID-Token")

        # get token with matching token id from DB so we can compare...
        token = await Token.get(token_id=int(token_header["kid"]))



        

        # if and ip got specified check it
        if ip is not None and (
            token_header["aud"] != ip or token_header["aud"] != token.ip
        ):
            raise ValueError("Token IP mismatch!")

        # check vhost
        if token.vhost != token_header.get("vhost", None):
            raise ValueError("VHost mismatch!")

        # verify the id token
        jwt.decode(
            id_jwt,
            token_config.decode_secret(token.sign_method),
            algorithms=token.sign_method.value,
        )

        # return the Token from the Database
        return token

    async def create_access_jwt(self, token_config: TokenConfig) -> str:
        """Creates an Access JWT

        It's expected that you verify the ID JWT beforehand with `Token.verify_token()`

        Args:
            token_config (TokenConfig): Config to use for creating a Token

        Returns:
            str: a JWT Token
        """

        usergroups = await (await self.user).groups.all().values_list("name", flat=True)

        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=token_config.access_lifetime
        )

        return jwt.encode(
            {"user": str(await self.user)},
            token_config.encode_secret(token_config.default_sign_method),
            headers={
                "iss": token_config.issuer,
                "exp": valid_until.timestamp(),
                "iat": datetime.datetime.now().timestamp(),
                "aud": usergroups,
                "Type": "Access-Token",
                "vhost": self.vhost,
            },
            algorithm=self.sign_method.value,
        )
