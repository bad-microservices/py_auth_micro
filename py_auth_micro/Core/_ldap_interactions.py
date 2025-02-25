from dataclasses import dataclass


try:
    import ldap  # type: ignore
except ImportError:
    print("cant import python-ldap\nldap connection won't work")

from ..Config import LDAPConfig


@dataclass
class LDAPHelper:
    """A class which helps interacting with an LDAP Server

    Warning:
        While instantiating this class it will bind against the LDAP!

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
        """Extracts the Users email after he sucessfully logged in (if he needs to be created in the Database)"""
        if self._userinfo.get("email", None) is None:
            return f"generated_{self.username}@{self.config.domain}"
        return self._userinfo["email"]

    def _get_user_info(self):
        connection_handler = _ConnectionHandler(
            self.config, self.username, self.password
        )
        with connection_handler as ldap_connection:
            userfilter = f"(&(objectClass=user)(sAMAccountName={self.username}))"
            _, data = ldap_connection.search_s(
                self.config.base_dn, ldap.SCOPE_SUBTREE, userfilter, None
            )[0]  # type: ignore
            groups_raw = data["memberOf"]
            groups = []
            for group in groups_raw:
                group = group.decode("utf-8")
                group = group[group.index("CN=") + 3 : group.index(",")]
                groups.append(group)

        mail = data.get("mail", None)
        if mail is not None:
            if isinstance(mail, list):
                mail = mail[0]
            if isinstance(mail, bytes):
                mail = mail.decode("utf-8")

        self._userinfo = {"groups": groups, "email": mail}

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
                valid_groups.append(group[len(self.config.groups_prefix) :])  # type: ignore

        return valid_groups

    def login(self) -> bool:
        """This Function checks if the User has the correct Usergroup to sign in.

        Returns:
            bool: True if the user is allowed to.
        """

        if self.config.group in self._userinfo["groups"]:
            return True

        return False


class _ConnectionHandler:
    config: LDAPConfig
    conn = None

    def __init__(self, ldap_config: LDAPConfig, username: str, password: str):
        self.config = ldap_config
        self.username = username
        self.password = password

    def __enter__(self):
        self.conn = ldap.initialize(self.config.address)
        self.conn.protocol_version = 3
        self.conn.set_option(ldap.OPT_REFERRALS, 0)
        # if a ca_file is specified create an tls context for ldaps
        if self.config.ca_file is not None:
            self.conn.set_option(ldap.OPT_X_TLS_CACERTFILE, self.config.ca_file)
            self.conn.set_option(ldap.OPT_X_TLS_NEWCTX, 0)

        username = f"{self.config.domain}\\{self.username}"
        self.conn.simple_bind_s(username, self.password)

        return self.conn

    def __exit__(self, *args):
        if self.conn is not None:
            self.conn.unbind_s()
