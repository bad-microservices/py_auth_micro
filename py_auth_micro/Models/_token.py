from tortoise import fields
from tortoise.models import Model

import datetime

from ..Core import SignMethod


class Token(Model):
    """Databse Entity Holding Information around issued Identity Tokens

    This Entity holds Information about issued Tokens. The Token ID is supplied in the JWT Header.
    A User can only have one valid Identity Token Per Time. A Token is bound to a vhost for the Message Broker.
    The Vhost is not specified in the Identity Token and only gets supplied in the Access Token.

    Args:
        Model (_type_): _description_
    """

    user: str = fields.ForeignKeyField(
        "models.User",
        related_name="token",
        pk=True,
        description="The User which relates to this Token",
    )
    token_id: int = fields.BigIntField(
        max_length=200, unique=True, description="ID of the Issued Token",index=True
    )
    ip: str = fields.CharField(
        max_length=39, description="IP That is valid for this User"
    )
    valid_until: datetime.datetime = fields.DatetimeField(
        auto_now_add=True, description="To what Time is this Token Valid", allows_generated=True, GENERATED_SQL = "NOW()"
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
