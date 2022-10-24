from ._loginbaseclass import LoginBaseClass
import bcrypt
from ..Models import User


class LoginLocal(LoginBaseClass):
    username: str
    password: str
    user: User = None

    async def login(self) -> bool:

        pw_hash = self.user.password_hash

        return bcrypt.checkpw(self.password.encode("utf-8"), pw_hash)
