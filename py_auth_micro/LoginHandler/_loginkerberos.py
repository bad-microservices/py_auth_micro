from ._loginbaseclass import LoginBaseClass
from ..Models import User

class LoginKerberos(LoginBaseClass):
    username: str
    password: str
    user: User = None

    async def login(self) -> bool:

        raise NotImplementedError
