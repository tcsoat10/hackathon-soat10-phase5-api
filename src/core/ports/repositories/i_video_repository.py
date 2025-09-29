from abc import ABC, abstractmethod
from typing import Any, Optional
from src.core.domain.dtos.list_videos_in import ListVideosIn
from src.core.domain.entities.video import Video

class IVideoRepository(ABC):
    @abstractmethod
    def save(self, video: Video) -> Video:
        pass
    
    @abstractmethod
    def find_by_job_ref(self, job_ref: str) -> Optional[Video]:
        pass
    
    @abstractmethod
    def list_videos_by_user(self, list_videos_in: ListVideosIn, client_identification: str) -> dict[str, Any]:
        pass


__all__ = ["IVideoRepository"]
