from tortoise import fields
from tortoise.models import Model

import datetime

class Token(Model):
    id = fields.BigIntField(pk=True)
    #user = fields.ForeignKeyField("models.User",related_name="token")
    token:str = fields.CharField(max_length=200,unique=True)
    ip:str = fields.CharField(max_length=39)
    valid_until:datetime.datetime = fields.DatetimeField()
    last_jwt: datetime.datetime = fields.DatetimeField(auto_now=True)
