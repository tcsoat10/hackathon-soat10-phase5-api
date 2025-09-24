from abc import ABC, abstractmethod
from typing import Optional
from src.core.domain.entities.video import Video

class IVideoRepository(ABC):
    @abstractmethod
    def save(self, video: Video) -> Video:
        pass
    
    @abstractmethod
    def find_by_job_ref(self, job_ref: str) -> Optional[Video]:
        pass
    
    @abstractmethod
    def list_videos_by_user(self, client_identification: str) -> list[Video]:
        pass


__all__ = ["IVideoRepository"]
