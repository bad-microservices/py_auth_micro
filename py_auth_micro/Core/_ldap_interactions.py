import ldap

from ..Config import LDAPConfig


class LDAPHelper:

    config: LDAPConfig = None

    def __init__(self, config: LDAPConfig):
        self.config = config

    def authenticate(self, username: str, password: str):
        conn = ldap.initialize(self.config.address)
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)
        # if a ca_file is specified create an tls context for ldaps
        if self.config.ca_file is not None:
            conn.set_option(ldap.OPT_X_TLS_CACERTFILE, self.config.ca_file)
            conn.set_option(ldap.OPT_X_TLS_NEWCTX, 0)

        username = f"{self.config.suffix}\{username}"
        conn.simple_bind_s(username, password)
        return conn

    def get_ldap_groups(self, username: str, password: str) -> list:

        ldap_c = self.authenticate(username, password)
        userfilter = f"(&(objectClass=user)(sAMAccountName={username}))"
        userresults = ldap_c.search_s(
            self.config.base_dn, ldap.SCOPE_SUBTREE, userfilter, None
        )[0][1]["memberOf"]
        groups = []
        for group in userresults:
            group = group.decode("utf-8")
            group = group[group.index("CN=") + 3 : group.index(",")]
            groups.append(group)
        return groups

    def login(self, username: str, password: str) -> bool:
        try:
            groups = self.get_ldap_groups(username, password)
            if self.config.group in groups:
                return True
            else:
                return False
        except Exception as err:
            return False
