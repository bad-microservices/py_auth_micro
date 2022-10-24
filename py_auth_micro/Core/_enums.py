from enum import Enum

class AuthSource(Enum):
    LOCAL = "LOCAL"
    LDAP = "LDAP"
    KERBEROS = "KERBEROS"
