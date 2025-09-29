from typing import Any, Optional
from src.core.domain.dtos.list_videos_in import ListVideosIn
from src.core.domain.entities.video import Video
from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.infrastructure.repositories.mongoengine.models.video_model import VideoModel

class MongoVideoRepository(IVideoRepository):

    def save(self, video: Video) -> Video:
        """Salva ou atualiza um Video."""
        if not video.id:
            model = VideoModel.from_entity(video)
        else:
            model = VideoModel.objects(id=video.id).first()
            if not model:
                raise ValueError(f"Video com ID {video.id} não encontrado para atualização.")

            model.status = video.status
            model.updated_at = video.updated_at

        model.save()
        model.reload()

        return model.to_entity()
    
    def find_by_job_ref(self, job_ref: str) -> Optional[Video]:
        """Encontra um Video pelo job_ref."""
        model: VideoModel = VideoModel.objects(job_ref=job_ref).first()
        return model.to_entity() if model else None

    def list_videos_by_user(self, list_videos_in: ListVideosIn, client_identification: str) -> dict[str, Any]:
        pipeline = [
            {"$match": {"client_identification": client_identification}},
            {"$sort": {"created_at": -1}},
            {"$facet": {
                "data": [{"$skip": (list_videos_in.page - 1) * list_videos_in.limit}, {"$limit": list_videos_in.limit}],
                "total": [{"$count": "count"}]
            }}
        ]

        result = VideoModel.objects.aggregate(*pipeline)
        videos = []
        total = 0
        for item in result:
            videos = [VideoModel.from_mongo(doc).to_entity() for doc in item.get("data", [])]
            total = item.get("total", [{}])[0].get("count", 0) if item.get("total") else 0

        return {
            "items": videos,
            "total": total,
            "page": list_videos_in.page,
            "limit": list_videos_in.limit
        }

__all__ = ["MongoVideoRepository"]
