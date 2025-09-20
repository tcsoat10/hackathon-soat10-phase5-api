
from pydantic import BaseModel


class SignInDTO(BaseModel):
    username: str
    password: str

__all__ = ["SignInDTO"]
