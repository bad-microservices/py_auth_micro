from ._loginbaseclass import LoginBaseClass
import bcrypt
from ..Models import User


class LoginLocal(LoginBaseClass):
    """Login Handler for Local Users

    Attributes:
        username (str): Username we want to authenticate.
        password (str): password for that specified user.
        user (User): Database instance of that user.

    Returns:
        _type_: _description_
    """
    username: str
    password: str
    user: User = None

    async def login(self) -> bool:
        """Hashes the users password and compares it against the Database.

        Note:
            Uses the `bcrypt` Module

        Returns:
            bool: Successfull Login
        """

        pw_hash = self.user.password_hash

        return bcrypt.checkpw(self.password.encode("utf-8"), pw_hash)
