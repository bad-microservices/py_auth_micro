from ._loginldap import LoginLDAP
from ._loginkerberos import LoginKerberos
from ._loginlocal import LoginLocal

from ..Core import AuthSource

LOGINHANDLER={
    AuthSource.LDAP : LoginLDAP,
    AuthSource.LOCAL : LoginLocal,
    AuthSource.KERBEROS : LoginKerberos
}