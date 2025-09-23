from typing import Optional
from uuid import uuid4
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

    def list_videos_by_user(self, client_identification: str) -> list[Video]:
        """Lista todos os vídeos enviados por um usuário específico."""
        models = VideoModel.objects(client_identification=client_identification)
        return [model.to_entity() for model in models]

__all__ = ["MongoVideoRepository"]
