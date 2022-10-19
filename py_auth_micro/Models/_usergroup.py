from tortoise import fields
from tortoise.models import Model


class UserGroup(Model):

    name: str = fields.CharField(unique=True, max_length=50, pk=True)
    members = fields.ManyToManyField(
        "models.UserGroup", related_name="groups", through="user_group_membership"
    )
