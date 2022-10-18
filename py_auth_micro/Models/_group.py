from tortoise import fields
from tortoise.models import Model

class Group(Model):
    id: fields.BigIntField(pk=True)
    name:str = fields.CharField(unique=True,max_length=50)
    #members = fields.ManyToManyField(
    #    "models.User", related_name="groups", through="group_user"
    #)