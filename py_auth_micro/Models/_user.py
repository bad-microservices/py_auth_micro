from tortoise import fields
from tortoise.models import Model
import datetime

from ..Core import AuthSource
class User(Model):

    username:str = fields.CharField(max_length=30, unique=True,pk=True, description="Username")
    password_hash:bytes = fields.BinaryField(description="Hash of the password (if local user)",null=True)
    auth_type: AuthSource = fields.CharEnumField(
        AuthSource,
        default=AuthSource.LOCAL,
        description="""What Kind of Authentification should be used for the User
Valid Options:
 - LOCAL
 - LDAP
 - KERBEROS""",
    )
    email:str = fields.CharField(max_length=100, unique=True,description="Email address for the user")
    activated:bool = fields.BooleanField(description="0: User did not verify his Email\n1: User verified his Email")
    created_at:datetime.datetime = fields.DatetimeField(auto_now_add=True,allows_generated=True,GENERATED_SQL="NOW()",description="When was this User added to the Database")
    modified_at:datetime.datetime = fields.DatetimeField(auto_now=True,allows_generated=True,GENERATED_SQL="NOW()",description="When was the user modified")
    

    token: fields.ReverseRelation["Token"]
    groups: fields.ReverseRelation["UserGroup"]
