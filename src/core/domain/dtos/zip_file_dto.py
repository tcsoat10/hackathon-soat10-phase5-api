from pydantic import BaseModel


class ZipFileDTO(BaseModel):
    job_ref: str
    client_identification: str
    file_url: str
    
    @classmethod
    def from_dict(cls, data: dict) -> "ZipFileDTO":
        return cls(**data)

__all__ = ["ZipFileDTO"]
