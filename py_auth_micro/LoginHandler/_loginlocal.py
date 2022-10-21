from ._loginbaseclass import LoginBaseClass
import bcrypt
from ..Models import User

class LoginLocal(LoginBaseClass):
    username: str
    password: str
    user: User = None
    
    async def login(self) -> bool:

        raise NotImplementedError
