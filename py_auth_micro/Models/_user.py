import logging
import datetime

from typing import Optional
from tortoise.fields import (
    Field,
    DatetimeField,
    CharField,
    CharEnumField,
    BinaryField,
    BooleanField,
    ManyToManyField,
    OneToOneRelation
)
from tortoise.models import Model
from jwt_helper import JWTEncoder

from py_auth_micro.Core import AuthSource
from py_auth_micro.Config import AppConfig
from py_auth_micro.Models._token import Token

logger = logging.getLogger(__name__)


class User(Model):
    """Model Representing a User

    Attributes:
        username (str): Name of the User.
        password_hash (str, optional): Passwordhash for local Users
        auth_type (AuthSource): How to authenticate the User.
        email (str): Email address of the User.
        activated (bool): User verified his email Address.
    """

    username: Field[str] = CharField(
        max_length=30, unique=True, primary_key=True, description="Username"
    )
    password_hash: Field[bytes] = BinaryField(
        description="Hash of the password (if local user)", null=True
    )
    auth_type: AuthSource = CharEnumField(
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
    email: Field[str] = CharField(
        max_length=100,
        unique=True,
        description="Email address for the user",
    )
    activated: Field[bool] = BooleanField(
        description="0: User did not verify his Email\n1: User verified his Email"
    )
    created_at: Field[datetime.datetime] = DatetimeField(
        auto_now_add=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was this User added to the Database",
    )
    modified_at: Field[datetime.datetime] = DatetimeField(
        auto_now=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was the user modified",
    )
    groups = ManyToManyField(
        model_name="models.Group",
        through="usergroup",
        related_name="users",
        forward_key="username",
        backward_key="name",
    )

    token: OneToOneRelation[Token]

    async def create_id_token(
        self,
        jwt_encoder: JWTEncoder,
        app_config: AppConfig,
        vhost: str = "/",
        ip: Optional[str] = "*",
    ) -> Token:
        """Creates a Token instance.

        Args:
            jwt_encoder (JWTEncoder): JWTEncoder instance which specifies the SigingMethod.
            app_config (AppConfig): AppConfig specifying the Lifetime of the Token.
            vhost (str, optional): For which VHost the Token is valid for. Defaults to "/".
            ip (str, optional): IP which the Token is bound to. Defaults to `*`.

        Returns:
            Token: _description_
        """
        logger.debug(f"creating token for {self.username}")
        # check if old Token exists
        token = await Token.get_or_none(user=self.username)

        # delete old token
        if token is not None:
            logger.debug(f"deleting old Token with id: {token.token_id}")
            await token.delete()

        valid_until = datetime.datetime.now(
            tz=datetime.timezone.utc
        ) + datetime.timedelta(minutes=app_config.id_token_valid_time)

        logger.debug(
            f"creating token for {self.username} with following specs:\nip: {ip}\nmethod: {jwt_encoder.signmethod.value}\nvhost: {vhost}\nvhost: {vhost}"
        )

        token = await Token.create(
            user=self,
            ip=ip,
            sign_method=jwt_encoder.signmethod,
            vhost=vhost,
            valid_until=valid_until,
        )

        return token

    async def revoke_id_token(self) -> bool:
        """Revokes the ID-Token by deleting the Database Entity Representing it.

        Returns:
            bool: The Token got revoked.
        """
        logger.debug(f"revoking ID-Token for {self.username}")
        if self.token is not None:
            await self.token.delete()
        return True

    def __str__(self):
        return self.username
