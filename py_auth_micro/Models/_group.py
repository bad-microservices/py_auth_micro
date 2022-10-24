from tortoise import fields
from tortoise.models import Model

from ._user import User


class Group(Model):
    """Database Model Representing a Group.

    Groups are used for Permission.

    Attributes:
        name (str): Name of the Usergroup
        users (list[User]): List of Users in this group
    """
    name: str = fields.CharField(unique=True, max_length=50, pk=True)
    users: fields.ManyToManyRelation[User]

    def __str__(self):
        return self.name
