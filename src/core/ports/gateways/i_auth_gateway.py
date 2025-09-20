
from abc import ABC, abstractmethod


class IAuthGateway(ABC):
    @abstractmethod
    def sign_up(self, person_data: dict, user_data: dict) -> dict:
        pass

    @abstractmethod
    def sign_in(self, email: str, password: str) -> dict:
        pass

__all__ = ["IAuthGateway"]
