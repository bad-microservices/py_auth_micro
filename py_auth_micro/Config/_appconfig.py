from dataclasses import dataclass


@dataclass
class AppConfig:
    """A class holding information about the general configuration State.

    Attributes:
        id_token_valid_time (int): How long ID Tokens stay valid (in minutes). Defaults to :code:`1440` (24 hours).
        access_token_valid_time (int): How long Access Tokens stay valid (in minutes). Defaults to :code:`5` .
        allow_registration (bool): Can users register themselfs?. Defaults to :code:`False` .
        auto_activate_accounts (bool): Automatically activate Accounts on creation. Defaults to :code:`True` .
        admin_group (str): Name of the administrator Group. Defaults to :code:`admin` .
        default_vhost (str): Name of the Default VHOST if no VHOST ist given on Login. Defaults to :code:`prod` .
        username_regex (str): Regex to check Usernames with. Defaults to :code:`r"[a-zA-Z-_0-9]{4,30}"` .
        password_regex (str): Regex to check Passwords with. Defaults to :code:`r".{4,}"` .
        email_regex (str): Regex to check Emails with. Defaults to a kinda long regex doing basic checks for emails.
    """

    id_token_valid_time: int = 1440
    access_token_valid_time: int = 5
    allow_registration: bool = False
    auto_activate_accounts: bool = True
    admin_group: str = "admin"
    default_vhost: str = "prod"
    group_regex: str = r"[a-zA-Z0-9_-]{1,50}"
    username_regex: str = r"[a-zA-Z-_0-9]{4,30}"
    password_regex: str = r".{4,}"
    email_regex: str = (
        r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)"
    )
