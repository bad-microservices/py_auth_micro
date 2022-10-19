from tortoise import fields
from tortoise.models import Model


class User(Model):

    username:str = fields.CharField(max_length=30, unique=True,pk=True)
    password_hash:bytes = fields.BinaryField()
    email:str = fields.CharField(max_length=100, unique=True)
    activated:bool = fields.BooleanField()
    
