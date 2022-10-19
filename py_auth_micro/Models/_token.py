from tortoise import fields
from tortoise.models import Model

import datetime

from ..Core import SignMethod, AuthSource


class Token(Model):

    user: str = fields.ForeignKeyField("models.User", related_name="token", pk=True)
    token_id: int = fields.BigIntField(max_length=200, unique=True)
    auth_type: AuthSource = fields.IntEnumField(AuthSource)
    ip: str = fields.CharField(max_length=39)
    valid_until: datetime.datetime = fields.DatetimeField(auto_now_add=True)
    last_use: datetime.datetime = fields.DatetimeField(auto_now=True)
    sign_method: SignMethod = fields.CharEnumField(SignMethod, max_length=10)
    vhost: str = fields.CharField(max_length=100, default="test")
