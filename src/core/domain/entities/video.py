from datetime import datetime
from typing import Optional

from src.core.domain.entities.base_entity import BaseEntity

class Video(BaseEntity):
    """Entidade que representa um vídeo salvo no S3."""

    def __init__(
        self,        
        client_identification: str,
        file_name: str,
        file_type: str,
        job_ref: Optional[str] = None,
        status: Optional[str] = None,
        email: Optional[str] = None,
        detail: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None,
        id: Optional[str] = None,
    ):
        super().__init__(
            id=id,
            created_at=created_at if created_at else datetime.now(),
            updated_at=updated_at if updated_at else datetime.now(),
            inactivated_at=inactivated_at
        )
        self.client_identification = client_identification
        self.job_ref = job_ref
        self.status = status
        self.email = email
        self.file_name = file_name
        self.file_type = file_type
        self.detail = detail

__all__ = ["Video"]
