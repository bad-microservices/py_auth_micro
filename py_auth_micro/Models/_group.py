from tortoise import fields
from tortoise.models import Model

class Group(Model):
    name:str = fields.CharField(unique=True,max_length=50,pk=True)
    members= fields.ManyToManyField(
        "models.Group", related_name="groups", through="group_user"
    )