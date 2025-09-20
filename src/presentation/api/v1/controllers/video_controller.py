from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.application.use_cases.upload_video_use_case import UploadVideoUseCase
from src.core.domain.dtos.video_dto import VideoDTO
from src.presentation.api.v1.presenters.dto_presenter import DTOPresenter


class VideoController:
    def __init__(self, video_repository: IVideoRepository):
        self._video_repository = video_repository

    async def upload_video(self, file, current_user):
        upload_video_use_case = UploadVideoUseCase.build(video_repository=self._video_repository)
        uploaded_video = await upload_video_use_case.execute(file=file, current_user=current_user)
        return DTOPresenter.transform(uploaded_video, VideoDTO)
