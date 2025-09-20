from mongoengine import StringField, DictField
from src.core.shared.identity_map import IdentityMap
from src.infrastructure.repositories.mongoengine.models.base_model import BaseModel
from src.core.constants.video_status import VideoStatusEnum
from src.core.domain.entities.video import Video


class VideoModel(BaseModel):
    """Modelo MongoEngine para Video."""
    meta = {'collection': 'videos', 'indexes': ['job_ref']}

    job_ref = StringField(required=True, unique=True)
    client_identification = StringField(required=True)
    status = StringField(required=True, choices=VideoStatusEnum.method_list())
    
    @classmethod
    def from_entity(cls, video: Video) -> "VideoModel":
        return cls(
            id=video.id,
            status=video.status,
            job_ref=video.job_ref if video.job_ref else '',
            client_identification=video.client_identification,
        )

    def to_entity(self) -> Video:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_entity: Video = identity_map.get(Video, self.id)
        if existing_entity:
            return existing_entity
        
        video = Video(
            id=str(self.id),
            job_ref=self.job_ref,
            client_identification=self.client_identification,
        )

        identity_map.add(video)
        return video

__all__ = ["VideoModel"]