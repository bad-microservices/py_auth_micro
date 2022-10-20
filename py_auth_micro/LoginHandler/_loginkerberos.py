from ._loginbaseclass import LoginBaseClass


class LoginKerberos(LoginBaseClass):
    username: str
    password: str

    def perform_login(self) -> bool:

        raise NotImplementedError
