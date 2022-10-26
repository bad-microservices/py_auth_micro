"""Some Core Modules used by other packages from this library.

Provides the Following classes:

    * :code:`AuthSource` - an enum specifying the Authentification source which should be used for a User.
    * :code:`LDAPHelper` - a class to simplify the interactions with an LDAP Server

"""

from ._enums import AuthSource
from ._ldap_interactions import LDAPHelper

__all__ = ["AuthSource", "LDAPHelper"]
