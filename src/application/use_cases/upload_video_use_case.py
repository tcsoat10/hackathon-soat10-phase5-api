from typing import Any
from fastapi import UploadFile

from src.core.domain.entities.video import Video
from src.core.ports.gateways.i_frame_extractor_gateway import IFrameExtractorGateway
from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.core.constants.video_status import VideoStatusEnum
from src.core.domain.dtos.register_video_dto import RegisterVideoDTO
from src.infrastructure.gateways.frame_extractor_gateway import FrameExtractorGateway
from config.settings import CALLBACK_URL, API_X_API_KEY


class UploadVideoUseCase:
    def __init__(
        self,
        video_repository: IVideoRepository,
        frame_extractor_gateway: IFrameExtractorGateway = FrameExtractorGateway()
    ):
        self.video_repository = video_repository
        self.frame_extractor_gateway = frame_extractor_gateway
        self.notify_url = f"{CALLBACK_URL}?api_key={API_X_API_KEY}"
    
    @classmethod
    def build(cls, video_repository: IVideoRepository, frame_extractor_gateway: IFrameExtractorGateway) -> "UploadVideoUseCase":
        return cls(video_repository=video_repository, frame_extractor_gateway=frame_extractor_gateway)

    async def execute(self, file: UploadFile, current_user: dict[str, Any]) -> Video:
        register_video_dto = RegisterVideoDTO(
            video_file=file,
            client_identification=current_user['person']['username'],
            notify_url=self.notify_url
        )
        
        video_response = self.frame_extractor_gateway.send_video_to_frame_extractor(register_video_dto)
        video = Video(
            client_identification=register_video_dto.client_identification,
            status=VideoStatusEnum.QUEUED_FRAMES.status,
            job_ref=video_response['job_ref'],
            email=current_user['person']['email']
        )
        video = self.video_repository.save(video)
        return video

__all__ = ["UploadVideoUseCase"]
