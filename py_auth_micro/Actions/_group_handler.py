from tortoise.exceptions import DoesNotExist
from ..Models import UserGroup

class GroupHandler:

    
    async def create_group(groupname:str):
        try:
            await UserGroup.get(name=groupname)
            raise ValueError("Group already Exists")
        except DoesNotExist:
            await UserGroup.create(name=groupname)

    async def create_groups(groupnames:list[str],ignore_exception:bool = False):
        pass
