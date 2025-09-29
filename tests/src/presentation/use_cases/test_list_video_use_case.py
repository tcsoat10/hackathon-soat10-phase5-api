import pytest
from unittest.mock import Mock
from src.application.use_cases.list_video_use_case import ListVideoUseCase
from src.core.domain.dtos.list_videos_in import ListVideosIn
from src.core.ports.repositories.i_video_repository import IVideoRepository

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
        
        expected_result = {
            "items": expected_videos,
            "total": 2,
            "page": 1,
            "limit": 10
        }
        
        self._video_repository.list_videos_by_user.return_value = expected_result
        
        mock = Mock(page=1, limit=10)
        result = await self._list_video_usecase.list_videos(list_videos_in=mock, client_identification=client_identification)
        
        self._video_repository.list_videos_by_user.assert_called_once_with(client_identification=client_identification, list_videos_in=mock)

        assert result == expected_result

    @pytest.mark.asyncio
    async def test_list_videos_failure(self, setup):
        client_identification = "testuser"
        
        self._video_repository.list_videos_by_user.side_effect = Exception("Database error")
        
        mock = Mock(spec=ListVideosIn, page=1, limit=10)
        
        with pytest.raises(Exception) as exc_info:
            await self._list_video_usecase.list_videos(client_identification=client_identification, list_videos_in=mock)

        self._video_repository.list_videos_by_user.assert_called_once_with(client_identification=client_identification, list_videos_in=mock)
        assert str(exc_info.value) == "Database error"

__all__ = ["TestListVideoUseCase"]
