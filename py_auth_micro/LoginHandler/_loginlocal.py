from ._loginbaseclass import LoginBaseClass


class LoginLocal(LoginBaseClass):
    username: str
    password: str

    def perform_login(self) -> bool:

        raise NotImplementedError
