from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from src.core.domain.entities.video import Video

class VideoDTO(BaseModel):
    id: str
    job_ref: str
    client_identification: str
    status: str
    created_at: datetime
    updated_at: datetime
    detail: Optional[str] = None
    filename: Optional[str] = None
    filetype: Optional[str] = None

    @classmethod
    def from_entity(cls, entity: Video) -> "VideoDTO":
        return cls( 
            id=str(entity.id),
            job_ref=entity.job_ref,
            client_identification=entity.client_identification,
            status=entity.status,
            filename=entity.file_name,
            filetype=entity.file_type,
            detail=entity.detail,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

__all__ = ["VideoDTO"]
