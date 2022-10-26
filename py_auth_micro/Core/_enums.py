from enum import Enum

class AuthSource(Enum):
    """Describes the Possible Authentification Sources Supported by this Library.
    """
    LOCAL = "LOCAL"
    """Is used for authenticating users from the app database"""
    LDAP = "LDAP"
    """Is used for authenticating users from an LDAP as Identity Provider."""
    KERBEROS = "KERBEROS"
    """Is used for authenticating users via Kerberos."""
