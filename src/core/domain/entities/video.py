from datetime import datetime
from typing import Dict, Optional, Any

from src.core.domain.entities.base_entity import BaseEntity
from src.core.constants.video_status import VideoStatusEnum

class Video(BaseEntity):
    """Entidade que representa um vídeo salvo no S3."""

    def __init__(
        self,        
        client_identification: str,     
        bucket: str,
        video_path: str,
        job_ref: Optional[str] = None,
        notification_url: Optional[str] = None,
    ):
        self.client_identification = client_identification        
        self.bucket = bucket        
        self.video_path = video_path
        self.job_ref = job_ref
        self.notification_url = notification_url

__all__ = ["Video"]
