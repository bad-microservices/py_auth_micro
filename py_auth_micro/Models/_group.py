from tortoise.fields import Field, CharField, ManyToManyRelation
from tortoise.models import Model

from py_auth_micro.Models._user import User


class Group(Model):
    """Database Model Representing a Group.

    Groups are used for Permission.

    Attributes:
        name (str): Name of the Usergroup
        users (list[User]): List of Users in this group
    """

    name: Field[str] = CharField(unique=True, max_length=50, primary_key=True)
    users: ManyToManyRelation[User]

    def __str__(self):
        return self.name
