import pytest
from unittest.mock import Mock
from src.application.use_cases.list_video_use_case import ListVideoUseCase
from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.core.domain.dtos.video_dto import VideoDTO

class TestListVideoUseCase:
    
    @pytest.fixture
    def setup(self):
        self._video_repository = Mock(spec=IVideoRepository)
        self._list_video_usecase = ListVideoUseCase.build(video_repository=self._video_repository)

    @pytest.mark.asyncio
    async def test_list_videos_success(self, setup):
        client_identification = "testuser"
        
        expected_videos = [
            Mock(id="video1", title="Video 1", url="http://example.com/video1"),
            Mock(id="video2", title="Video 2", url="http://example.com/video2")
        ]
        
        self._video_repository.list_videos_by_user.return_value = expected_videos
        
        videos = await self._list_video_usecase.list_videos(client_identification=client_identification)
        
        self._video_repository.list_videos_by_user.assert_called_once_with(client_identification=client_identification)
        assert len(videos) == 2
        assert all(isinstance(video, Mock) for video in videos)
        
    @pytest.mark.asyncio
    async def test_list_videos_failure(self, setup):
        client_identification = "testuser"
        
        self._video_repository.list_videos_by_user.side_effect = Exception("Database error")
        
        with pytest.raises(Exception) as exc_info:
            await self._list_video_usecase.list_videos(client_identification=client_identification)

        self._video_repository.list_videos_by_user.assert_called_once_with(client_identification=client_identification)
        assert str(exc_info.value) == "Database error"

__all__ = ["TestListVideoUseCase"]
