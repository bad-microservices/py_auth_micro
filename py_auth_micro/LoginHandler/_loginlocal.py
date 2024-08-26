import bcrypt
import logging

from ..Models import User
from ._loginbaseclass import LoginBaseClass


class LoginLocal(LoginBaseClass):
    """Login Handler for Local Users

    Attributes:
        username (str): Username we want to authenticate.
        password (str): password for that specified user.
        user (User): Database instance of that user.
    """

    username: str
    password: str
    user: User

    async def login(self) -> bool:
        """Hashes the users password and compares it against the Database.

        Note:
            Uses the :code:`bcrypt` Module

        Returns:
            bool: Successfull Login
        """
        logger = logging.getLogger(__name__)
        logger.debug(f"tyring to login {self.username} Localy")

        pw_hash = self.user.password_hash

        pw_matches = bcrypt.checkpw(self.password.encode("utf-8"), pw_hash)

        logger.debug(f"PW matches for User '{self.username}': {pw_matches}")

        return pw_matches
