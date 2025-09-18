from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.domain.entities.video import Video

class IVideoRepository(ABC):
    @abstractmethod
    def save(self, video: Video) -> Video:
        pass
    
    '''
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Video]:
        pass

    @abstractmethod
    def get_by_job_ref(self, job_ref: str) -> Optional[Video]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str, skip: int = 0, limit: int = 10) -> List[Video]:
        pass

    @abstractmethod
    def find_by_filename(self, user_id: str, filename: str) -> Optional[Video]:        
        pass

    @abstractmethod
    def update_status(self, job_ref: str, status: str) -> Optional[Video]:        
        pass

    @abstractmethod
    def delete(self, video_id: str) -> bool:        
        pass
    '''


__all__ = ["IVideoRepository"]