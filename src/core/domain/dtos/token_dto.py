from pydantic import BaseModel

class TokenDTO(BaseModel):
    access_token: str
    token_type: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            access_token=data.get("access_token"),
            token_type=data.get("token_type"),
        )

__all__ = ["TokenDTO"]
