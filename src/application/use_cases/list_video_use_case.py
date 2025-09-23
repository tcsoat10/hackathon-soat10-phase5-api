from src.core.ports.repositories.i_video_repository import IVideoRepository


class ListVideoUseCase:

    def __init__(self, video_repository: IVideoRepository):
        self._video_repository: IVideoRepository = video_repository

    @classmethod
    def build(cls, video_repository: IVideoRepository):
        return cls(video_repository=video_repository)

    async def list_videos(self, client_identification: str):
        return self._video_repository.list_videos_by_user(client_identification=client_identification)
