from pydantic import BaseModel
from typing import Any, List
from src.core.domain.dtos.video_dto import VideoDTO

class ListVideosOut(BaseModel):
    items: List[VideoDTO]
    total: int
    page: int
    limit: int

    @classmethod
    def from_entity(cls, list_videos_out: dict[str, Any]) -> "ListVideosOut":
        return cls(
            items=list_videos_out['items'],
            total=list_videos_out['total'],
            page=list_videos_out['page'],
            limit=list_videos_out['limit']
        )

__all__ = ["ListVideosOut"]
