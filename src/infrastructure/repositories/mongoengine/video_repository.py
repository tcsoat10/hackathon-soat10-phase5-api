from typing import Optional
from uuid import uuid4
from src.core.domain.entities.video import Video
from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.infrastructure.repositories.mongoengine.models.video_model import VideoModel

class MongoVideoRepository(IVideoRepository):

    def save(self, video: Video) -> Video:
        """Salva ou atualiza um Video."""
        if not video.id:
            video.id = str(uuid4())
            model = VideoModel.from_entity(video)
        else:
            model = VideoModel.objects(id=video.id).first()
            if not model:
                raise ValueError(f"Video com ID {video.id} não encontrado para atualização.")

            model.status = video.status
            model.bucket = video.bucket
            model.frames_path = video.frames_path
            model.notification_url = video.notification_url
            model.updated_at = video.updated_at

        model.save()

        return model.to_entity()
    
__all__ = ["MongoZipJobRepository"]