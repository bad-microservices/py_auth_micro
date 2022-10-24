from dataclasses import dataclass

@dataclass
class AppConfig:
    """A class holding information about the general configuration State.

    Attirbutes:
        id_token_valid_time (int): How long ID Tokens stay valid (in minutes). Defaults to `1440` (24 hours).
        access_token_valid_time (int): How long Access Tokens stay valid (in minutes). Defaults to `5`.
        allow_registration (bool): Can users register themselfs?. Defaults to `False`.
        auto_activate_accounts (bool): Automatically activate Accounts on creation. Defaults to `True`
        admin_group (str): Name of the administrator Group. Defaults to `admin`
        username_regex (str): Regex to check Usernames with. Defaults to `r"[a-zA-Z-_0-9]{4,30}"`
        password_regex (str): Regex to check Passwords with. Defaults to `r".{4,}"`
        email_regex (str): Regex to check Emails with. Defaults to a kinda long regex doing basic checks for emails.
    """
    id_token_valid_time:int = 1440
    access_token_valid_time:int = 5
    allow_registration: bool = False
    auto_activate_accounts: bool = True
    admin_group: str = "admin"
    username_regex: str = r"[a-zA-Z-_0-9]{4,30}"
    password_regex: str = r".{4,}"
    email_regex: str = r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)"
