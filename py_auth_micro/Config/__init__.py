"""This SubModule holds different Config Classes needed for the package.

The Following Config Classes are provided:

    * :code:`LDAPConfig` - for configuring the LDAP Connection.
    * :code:`DBConfig` - for configuring the DB Connection.
    * :code:`AppConfig` - for general Settings regarding this Package.

"""
from py_auth_micro.Config._ldapconfig import LDAPConfig
from py_auth_micro.Config._dbconfig import DBConfig
from py_auth_micro.Config._appconfig import AppConfig

__all__ = ["LDAPConfig", "DBConfig","AppConfig"]
