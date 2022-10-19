from tortoise import fields
from tortoise.models import Model

import datetime

class Token(Model):
    user:str = fields.ForeignKeyField("models.User",related_name="token",pk=True)
    token:str = fields.CharField(max_length=200,unique=True)
    ip:str = fields.CharField(max_length=39)
    valid_until:datetime.datetime = fields.DatetimeField()
    last_use: datetime.datetime = fields.DatetimeField(auto_now=True)
    sign_method: 
