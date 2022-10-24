import re
import datetime

from typing import Optional
from tortoise import fields
from tortoise.models import Model
from jwt_helper import JWTEncoder

from ..Core import AuthSource
from ..Config import AppConfig
from ._token import Token


class User(Model):

    username: str = fields.CharField(
        max_length=30, unique=True, pk=True, description="Username"
    )
    password_hash: bytes = fields.BinaryField(
        description="Hash of the password (if local user)", null=True
    )
    auth_type: AuthSource = fields.CharEnumField(
        AuthSource,
        default=AuthSource.LOCAL,
        description=(
            "What Kind of Authentification should be used for the User"
            "Valid Options:"
            " - LOCAL"
            " - LDAP"
            " - KERBEROS"
        ),
    )
    email: str = fields.CharField(
        max_length=100,
        unique=True,
        description="Email address for the user",
    )
    activated: bool = fields.BooleanField(
        description="0: User did not verify his Email\n1: User verified his Email"
    )
    created_at: datetime.datetime = fields.DatetimeField(
        auto_now_add=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was this User added to the Database",
    )
    modified_at: datetime.datetime = fields.DatetimeField(
        auto_now=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was the user modified",
    )
    groups = fields.ManyToManyField(
        model_name="models.Group",
        through="usergroup",
        related_name="users",
        forward_key="username",
        backward_key="name",
    )

    token: fields.ReverseRelation[Token]

    async def create_id_token(
        self,
        jwt_encoder: JWTEncoder,
        app_config: AppConfig,
        vhost: str = "/",
        ip: Optional[str] = None,
    ) -> "Token":
        # check if old Token exists
        token = await Token.get_or_none(user=self.username)

        # delete old token
        if token is not None:
            await token.delete()

        valid_until = datetime.datetime.now(
            tz=datetime.timezone.utc
        ) + datetime.timedelta(minutes=app_config.id_token_valid_time)

        token = await Token.create(
            user=self,
            ip=ip,
            sign_method=jwt_encoder.default_sign_method,
            vhost=vhost,
            valid_until=valid_until,
        )

        return token

    async def revoke_id_token(self) -> bool:
        if self.token is not None:
            await self.token.delete()
        return True

    def __str__(self):
        return self.username
