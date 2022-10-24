from dataclasses import dataclass

@dataclass
class AppConfig:
    allow_registration:bool = False
    auto_activate_accounts:bool = True
    admin_group:str = "admin"
    username_regex:str = r"[a-zA-Z-_0-9]{4,30}"
    password_regex:str = r".{4,}"
    email_regex:str = r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)"