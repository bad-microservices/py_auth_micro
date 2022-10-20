from ._loginbaseclass import LoginBaseClass


class LoginLocal(LoginBaseClass):
    username: str
    password: str

    def perform_login() -> bool:

        raise NotImplementedError
