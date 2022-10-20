from tortoise import fields
from tortoise.models import Model


class UserGroup(Model):

    name: str = fields.CharField(unique=True, max_length=50, pk=True)
    members: fields.ManyToManyRelation["User"]

    def __str__(self):
        return self.name
