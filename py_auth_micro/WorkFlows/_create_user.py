from tortoise.exceptions import DoesNotExist
from typing import Optional
import bcrypt
from ..Models import User
from ..Core import AuthSource
from ..Exceptions import AlreadyExists


async def create_user(
    username: str, password: str, email: str, activated: bool = False
) -> User:

    # check if username or email is already taken
    try:
        await User.get(username=username)
        raise AlreadyExists("username already Taken")
    except DoesNotExist:
        pass

    try:
        await User.get(email=email)
        raise AlreadyExists("email is already Taken")
    except DoesNotExist:
        pass

    # create password hash
    pw_salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)

    # now we can actualy create the user
    usr = await User.create(
        username=username, email=email, activated=activated, password_hash=pw_hash
    )
    return usr

async def delete_user(username:str) -> bool:

    await(await User.get(username=username)).delete()
    return True

async def change_user(username:str,**kwargs) -> User:
    user = await User.get(username=username)

    pass