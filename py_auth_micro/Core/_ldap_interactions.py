from dataclasses import dataclass
try:
    import ldap
except ImportError:
    print("cant import python-ldap\nldap connection wont work")

from ..Config import LDAPConfig


@dataclass
class LDAPHelper:
    """A class which helps interacting with an LDAP Server

    Warning:
        While instantiating this class it will bin against the LDAP!

    Attributes:
        config (LDAPConfig): The Configuration to connect to the LDAP.
        username (str): Name of the User we want to log in with.
        password (str): Password of the user.
    """

    config: LDAPConfig
    username: str
    password: str
    _userinfo: dict

    @property
    def email(self):
        """Extracts the Users email after he sucessfully logged in (if he needs to be created in the Database)
        """
        return self._userinfo["email"]

    def _get_connection(self):
        conn = ldap.initialize(self.config.address)
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)
        # if a ca_file is specified create an tls context for ldaps
        if self.config.ca_file is not None:
            conn.set_option(ldap.OPT_X_TLS_CACERTFILE, self.config.ca_file)
            conn.set_option(ldap.OPT_X_TLS_NEWCTX, 0)

        username = f"{self.config.domain}\\{self.username}"
        conn.simple_bind_s(username, self.password)
        return conn

    def _get_user_info(self):
        ldap_connection = self._get_connection()
        userfilter = f"(&(objectClass=user)(sAMAccountName={self.username}))"
        _, data = ldap_connection.search_s(
            self.config.base_dn, ldap.SCOPE_SUBTREE, userfilter, None
        )[0]
        groups_raw = data["memberOf"]
        groups = []
        for group in groups_raw:
            group = group.decode("utf-8")
            group = group[group.index("CN=") + 3 : group.index(",")]
            groups.append(group)

        try:
            mail = data["mail"][0]
        except IndexError:
            mail = data["mail"]

        self._userinfo = {"groups": groups, "email": mail.decode("utf-8")}

    def __init__(self, ldap_cfg: LDAPConfig, username: str, password: str):
        self.config = ldap_cfg
        self.username = username
        self.password = password

        self._get_user_info()

    def get_groups(self) -> list:
        """This function will return a list of all relevant Groups.

        Returns:
            list: List of Usergroups
        """
        valid_groups = []
        for group in self._userinfo["groups"]:
            if group.startswith(self.config.groups_prefix):
                valid_groups.append(group[len(self.config.groups_prefix) :])

        return valid_groups

    def login(self) -> bool:
        """This Function checks if the User has the correct Usergroup to sign in.

        Returns:
            bool: True if the user is allowed to.
        """

        if self.config.group in self._userinfo["groups"]:
            return True

        return False
