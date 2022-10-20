from tortoise.exceptions import DoesNotExist
from ..Models import UserGroup

class GroupFunctions:

    
    async def create_group(groupname:str):
        try:
            await UserGroup.get(name=groupname)
            raise ValueError("Group already Exists")
        except DoesNotExist:
            await UserGroup.create(name=groupname)

    async def create_groups(groupnames:list[str],ignore_exceptions:bool = False):
        
        for group in groupnames:
            try:
                GroupFunctions.create_group(group)
            except DoesNotExist as exc:
                #reraise Exception if we dont ignore them
                if not ignore_exceptions:
                    raise exc
    
    async def add_user_to_group(username:str,groupname:str):
        pass

    async def add_user_to_groups(username:str,groupnames:list[str],ignore_exceptions:bool = False):

        for group in groupnames:
            try:
                await GroupFunctions.add_user_to_group(username,group)
            except DoesNotExist as exc:
                #reraise Exception if we dont ignore them
                if not ignore_exceptions:
                    raise exc

    async def remove_user_from_group(username:str,groupname:str):
        pass

    async def remove_user_from_groups(username:str,groupnames:str,ignore_exceptions:bool = False):
        for group in groupnames:
            try:
                await GroupFunctions.remove_user_from_groups(username,group)
            except DoesNotExist as exc:
                #reraise Exception if we dont ignore them
                if not ignore_exceptions:
                    raise exc

