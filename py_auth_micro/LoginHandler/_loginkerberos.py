from ._loginbaseclass import LoginBaseClass


class LoginKerberos(LoginBaseClass):
    username: str
    password: str

    def perform_login() -> bool:

        raise NotImplementedError
