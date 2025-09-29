from pydantic import BaseModel, Field, field_validator

class ListVideosIn(BaseModel):
    page: int = Field(1, description="Número da página")
    limit: int = Field(10, description="Limite de vídeos por página")
    
    @field_validator("page")
    def validate_page(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Page must be a positive integer.")
        return value

    @field_validator("limit")
    def validate_limit(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Limit must be a positive integer.")
        return value

__all__ = ["ListVideosIn"]
