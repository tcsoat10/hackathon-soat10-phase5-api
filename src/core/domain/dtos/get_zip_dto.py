from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, field_validator


class GetZipDTO(BaseModel):
    job_ref: str = Query(..., description="Identificador único do job")

    @field_validator("job_ref")
    def validate_job_ref_format(cls, value: str) -> str:
        try:
            UUID(value, version=4)
        except ValueError:
            raise ValueError("job_ref must be a valid UUID4 format.")

        return value

__all__ = ["GetZipDTO"]
