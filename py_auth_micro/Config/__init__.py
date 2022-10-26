"""This SubModule holds different Config Classes needed for the package.

The Following Config Classes are provided:

    * :code:`LDAPConfig` - for configuring the LDAP Connection.
    * :code:`DBConfig` - for configuring the DB Connection.
    * :code:`AppConfig` - for general Settings regarding this Package.

"""
from ._ldapconfig import LDAPConfig
from ._dbconfig import DBConfig
from ._appconfig import AppConfig

__all__ = ["LDAPConfig", "DBConfig","AppConfig"]
