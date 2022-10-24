from dataclasses import dataclass


@dataclass
class LDAPConfig:
    """a Configuration class storing our AD Related config

    Attributes:
        address (str): Server Address.
        base_dn (str): Base DN for Users.
        group (str, optional): Group that allows the Login itself. Defaults to "allowed_to_login".
        groups_prefix (str, optional): Prefix of groups that should be added to the User. Defaults to "API_PERM".
        domain (str, optional): The Domain the user should log into. Defaults to 3306.
        ca_file (str, optional): Path to the CA File used for ldaps. Defaults to None.
    """

    address: str = "ldap://127.0.0.1:389"
    base_dn: str = "ou=User,dc=ad,dc=local"
    group: str = "allowed_to_login"
    groups_prefix: str = "API_PERM"
    domain: str = "ad.local"
    ca_file: str = None