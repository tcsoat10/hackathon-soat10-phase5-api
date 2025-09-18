from pydantic import BaseModel
from datetime import datetime

from src.core.domain.entities.video import Video

class VideoDTO(BaseModel):
    id: str
    job_ref: str
    client_identification: str
    bucket: str
    frames_path: str
    notification_url: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: Video) -> "VideoDTO":
        return cls(
            id=str(entity.id),
            job_ref=entity.job_ref,
            client_identification=entity.client_identification,
            bucket=entity.bucket,
            frames_path=entity.frames_path,
            notification_url=entity.notification_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

__all__ = ["VideoJobDTO"]
