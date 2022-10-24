from enum import Enum

class AuthSource(Enum):
    """Describes the Possible Authentification Sources Supported by this Library.

    Attirbutes:
        LOCAL (str): Is used for authenticating users from the app database.
        LDAP (str): Is used for authenticating users from an LDAP as Identity Provider.
        KERBEROS (str): Is used for authenticating users via Kerberos.
    """
    LOCAL = "LOCAL"
    LDAP = "LDAP"
    KERBEROS = "KERBEROS"
