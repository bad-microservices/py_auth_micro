from dataclasses import dataclass
from typing import Union

from jwt_helper import SignMethod

@dataclass
class AppConfig:
    id_token_valid_time:int = 1440
    access_token_valid_time:int = 5
    allow_registration: bool = False
    auto_activate_accounts: bool = True
    admin_group: str = "admin"
    username_regex: str = r"[a-zA-Z-_0-9]{4,30}"
    password_regex: str = r".{4,}"
    email_regex: str = r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)"
