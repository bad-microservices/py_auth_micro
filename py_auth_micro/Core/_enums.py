from enum import Enum


class SignMethod(Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"


class AuthSource(Enum):
    LOCAL = "LOCAL"
    LDAP = "LDAP"
    KERBEROS = "KERBEROS"
