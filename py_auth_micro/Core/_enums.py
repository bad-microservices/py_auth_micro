from enum import Enum
from ..LoginHandler import LoginLocal, LoginLDAP, LoginKerberos


class SignMethod(Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    PS256 = "PS256"
    PS384 = "PS384"
    PS512 = "PS512"


class AuthSource(Enum):
    LOCAL = "LOCAL"
    LDAP = "LDAP"
    KERBEROS = "KERBEROS"
