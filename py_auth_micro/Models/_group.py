from tortoise import fields
from tortoise.models import Model

from ._user import User


class Group(Model):

    name: str = fields.CharField(unique=True, max_length=50, pk=True)
    users: fields.ManyToManyRelation[User]

    def __str__(self):
        return self.name
