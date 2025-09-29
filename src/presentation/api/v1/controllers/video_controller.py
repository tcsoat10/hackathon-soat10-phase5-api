from typing import Any
from src.core.domain.dtos.list_videos_in import ListVideosIn
from src.core.domain.dtos.list_videos_out import ListVideosOut
from src.core.ports.gateways.i_frame_extractor_gateway import IFrameExtractorGateway
from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.application.use_cases.upload_video_use_case import UploadVideoUseCase
from src.application.use_cases.list_video_use_case import ListVideoUseCase
from src.core.domain.dtos.video_dto import VideoDTO
from src.presentation.api.v1.presenters.dto_presenter import DTOPresenter


class VideoController:
    def __init__(self, video_repository: IVideoRepository, frame_extractor_gateway: IFrameExtractorGateway):
        self._video_repository = video_repository
        self._frame_extractor_gateway = frame_extractor_gateway

    async def upload_video(self, file, current_user):
        upload_video_use_case = UploadVideoUseCase.build(
            video_repository=self._video_repository,
            frame_extractor_gateway=self._frame_extractor_gateway
        )
        uploaded_video = await upload_video_use_case.execute(file=file, current_user=current_user)
        return DTOPresenter.transform(uploaded_video, VideoDTO)
    
    async def list_videos(self, list_videos_in: ListVideosIn, current_user: dict):
        list_video_use_case = ListVideoUseCase.build(video_repository=self._video_repository)
        list_videos_out: dict[str, Any] = await list_video_use_case.list_videos(list_videos_in=list_videos_in, client_identification=current_user['person']['username'])
        list_videos_out['items'] = [DTOPresenter.transform(video, VideoDTO) for video in list_videos_out['items']]
        return DTOPresenter.transform(list_videos_out, ListVideosOut)
    
__all__ = ["VideoController"]
    
