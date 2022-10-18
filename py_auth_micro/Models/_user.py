from tortoise import fields
from tortoise.models import Model


class User(Model):
    id:int = fields.BigIntField(pk=True)
    username:str = fields.CharField(max_length=30, unique=True)
    password_hash:bytes = fields.BinaryField()
    email:str = fields.CharField(max_length=100, unique=True)
    activated:bool = fields.BooleanField()
    #token = fields.ForeignKeyField("models.Token",related_name="user")
    #groups= fields.ManyToManyField(
    #    "models.Group", related_name="members", through="group_user"
    #)
