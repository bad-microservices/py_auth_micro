import logging
import datetime

from tortoise import fields
from tortoise.models import Model
from typing import Optional
from jwt_helper import SignMethod, JWTEncoder, JWTValidator

from ..Config import AppConfig


class Token(Model):
    """Databse Entity Holding Information around issued Identity Tokens

    This Entity holds Information about issued Tokens. The Token ID is supplied in the JWT Header.
    A User can only have one valid Identity Token Per Time. A Token is bound to a vhost for the Message Broker.
    The Vhost is not specified in the Identity Token and only gets supplied in the Access Token.

    Attributes:
        user (User): Relation to the User Object.
        token_id (int): A Unique ID for our issued Identity Tokens. (kid claim)
        ip (str): Ip which is valid for the Token. (Used for verification)
        valid_until (datetime.datetime): We store the validity of the Token in the Database as well
                so we can check the Tokens "exp" claim and in out Database to make sure it did not get forged (Trust me Bro!).
        last_use (datetime.datetime): Timestamp of the last Access-Token generation.
        sign_method (SignMethod): Method used to sign the ID-Token.
                (should be checked against the supported Mehtods of the JWTValidator)
        vhost (str): Identifies the VHOST of the RabbitMQ Server.
                    For example `prod` for the Production VHOST and `test` for the Test VHOST.
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

    async def get_id_jwt(self, jwt_encoder: JWTEncoder, app_cfg: AppConfig) -> str:
        """This Function will create a new ID-JWT

        Args:
            jwt_encoder (JWTEncoder): JWTEncoder which should be used to create the Token.
            app_cfg (AppConfig): Some misc. Config (important for the Validity duration of the Token)

        Returns:
            str: The ID-JWT
        """
        logger = logging.getLogger(__name__)
        logger.info(f"creating ID-Token JWT with id: {self.token_id}")
        usergroups = await self.user.groups.all().values_list("name", flat=True)

        token = jwt_encoder.create_jwt(
            {
                "kid": str(self.token_id),
                "aud": self.ip,
                "vhost": self.vhost,
                "type": "ID-Token",
            },
            {"groups": usergroups, "username": str(self.user)},
            app_cfg.id_token_valid_time,
        )
        logger.debug(f"token: {token}")
        return token

    @staticmethod
    async def verify_id_jwt(
        jwt_validator: JWTValidator,
        id_jwt: str,
        ip: Optional[str] = None,
    ):
        """Checks an ID-JWT

        Looks up the `kid` Claim from the Token Header and will validate the
        Token against the Token described in the Database.

        Args:
            jwt_validator (JWTValidator): JWT-Validator holding Information about our trusted Issuers (should contain ourself)
            id_jwt (str): The JWT to verify
            ip (Optional[str], optional): IP-Address of the Requesting Party. Defaults to None. (is not checked against if its None)

        Raises:
            ValueError: Token is not valid or does not Match data in DB.

        Returns:
            Token: the matched Database Token instance.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"verifying ID-Token from {ip}")
        logger.debug(f"token: {id_jwt}")
        token_content = jwt_validator.get_jwt_as_dict(id_jwt)

        token_header = token_content["headers"]

        logger.debug(f"token-headers: {token_header}")

        if token_header["type"] != "ID-Token":
            raise ValueError("not an ID-Token")

        # get token with matching token id from DB so we can compare...
        token = await Token.get(token_id=int(token_header["kid"]))

        # if and ip got specified check it
        if ip is not None and (
            token_header["aud"] != ip or token_header["aud"] != token.ip
        ):
            logger.error("Token IP missmatch!")
            raise ValueError("Token IP missmatch!")

        # check vhost
        if token.vhost != token_header.get("vhost", None):
            logger.error("VHost missmatch!")
            raise ValueError("VHost missmatch!")

        logger.info("Token is valid")
        # return the Token from the Database
        return token

    async def create_access_jwt(
        self, jwt_encoder: JWTEncoder, app_cfg: AppConfig
    ) -> str:
        """Creates an Access JWT

        It's expected that you verify the ID JWT beforehand with `Token.verify_token()`

        Args:
            jwt_encoder (JWTEncoder: JWT Encoder to use for creating the token

        Returns:
            str: a JWT Token
        """
        logger = logging.getLogger(__name__)
        logger.info("creating Access-Token")
        usergroups = await (await self.user).groups.all().values_list("name", flat=True)
        logger.debug(f"Token Groups: {usergroups}")
        return jwt_encoder.create_jwt(
            {
                "aud": usergroups,
                "Type": "Access-Token",
                "vhost": self.vhost,
            },
            {"user": str(await self.user)},
            app_cfg.access_token_valid_time,
        )
