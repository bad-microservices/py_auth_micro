from ._loginbaseclass import LoginBaseClass
from ..Config import LDAPConfig


class LoginLDAP(LoginBaseClass):
    ldap_config: LDAPConfig
    username: str
    password: str

    def perform_login() -> bool:

        return False
