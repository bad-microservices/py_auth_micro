from abc import ABC, abstractmethod

class LoginHandler(ABC):

    @abstractmethod
    def perform_login()->bool:
        pass
