from io import BytesIO
import pytest

from unittest.mock import Mock
from src.application.use_cases.upload_video_use_case import UploadVideoUseCase
from src.core.ports.gateways.i_frame_extractor_gateway import IFrameExtractorGateway
from src.core.ports.repositories.i_video_repository import IVideoRepository
from fastapi import UploadFile

class TestUploadVideoUseCase:
    
    @pytest.fixture
    def setup(self):
        self._video_repository = Mock(spec=IVideoRepository)
        self._frame_extractor_gateway = Mock(spec=IFrameExtractorGateway)
        self._upload_video_usecase = UploadVideoUseCase.build(
            video_repository=self._video_repository,
            frame_extractor_gateway=self._frame_extractor_gateway
        )

    @pytest.mark.asyncio
    async def test_upload_video_success(self, setup):
        file = Mock(spec=UploadFile)
        file.filename = "testvideo.mp4"
        file.content_type = "video/mp4"
        
        current_user = {
            "person": {
                "username": "testuser",
                "email": "testuser@example.com",
                "full_name": "Test User"
            }
        }
        
        expected_video = Mock()
        expected_video.id = "video123"
        expected_video.title = "Test Video"
        expected_video.url = "http://example.com/video123"
        expected_video.client_identification = "testuser"
        expected_video.status = "QUEUED_FRAMES"
        expected_video.job_ref = "jobref123"
        expected_video.email = "testuser@example.com"

        self._video_repository.save.return_value = expected_video
        self._frame_extractor_gateway.send_video_to_frame_extractor.return_value = {'job_ref': 'jobref123'}
        
        video = await self._upload_video_usecase.execute(file=file, current_user=current_user)
        
        self._video_repository.save.assert_called_once()
        self._frame_extractor_gateway.send_video_to_frame_extractor.assert_called_once()
        
        assert video.id == "video123"
        assert video.title == "Test Video"
        assert video.url == "http://example.com/video123"
        assert video.client_identification == "testuser"
        assert video.status == "QUEUED_FRAMES"
        assert video.job_ref == "jobref123"
        assert video.email == "testuser@example.com"

    @pytest.mark.asyncio
    async def test_upload_video_failure(self, setup):
        file = Mock(spec=UploadFile)
        file.filename = "testvideo.mp4"
        file.content_type = "video/mp4"
        
        current_user = {
            "person": {
                "username": "testuser",
                "email": "testuser@example.com",
                "full_name": "Test User"
            }
        }
        
        self._frame_extractor_gateway.send_video_to_frame_extractor.side_effect = Exception("Frame extractor service error")
        
        with pytest.raises(Exception) as exc_info:
            await self._upload_video_usecase.execute(file=file, current_user=current_user)
            
        self._frame_extractor_gateway.send_video_to_frame_extractor.assert_called_once()
        assert str(exc_info.value) == "Frame extractor service error"
