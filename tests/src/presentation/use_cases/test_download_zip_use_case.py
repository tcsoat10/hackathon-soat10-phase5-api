import pytest

from unittest.mock import Mock

from src.application.use_cases.download_zip_use_case import DownloadZipUseCase
from src.core.ports.gateways.i_zip_gateway import IZipGateway


class TestDownloadZipUseCase:
    
    @pytest.fixture
    def setup(self):
        self._zip_gateway = Mock(spec=IZipGateway)
        self._download_zip_usecase = DownloadZipUseCase.build(zip_gateway=self._zip_gateway)
        
    @pytest.mark.asyncio
    async def test_execute_success(self, setup):
        get_zip_dto = Mock()
        get_zip_dto.zip_id = "testzipid"
        
        current_user = {
            "person": {
                "username": "testuser"
            }
        }
        
        expected_response = b"somebinarydatarepresentingzipfile"
        
        self._zip_gateway.download_zip.return_value = expected_response
        
        zip_data = await self._download_zip_usecase.execute(get_zip_dto, current_user)
        
        self._zip_gateway.download_zip.assert_called_once_with(get_zip_dto, "testuser")
        assert zip_data == expected_response
        
    @pytest.mark.asyncio
    async def test_execute_failure(self, setup):
        get_zip_dto = Mock()
        get_zip_dto.zip_id = "invalidzipid"
        
        current_user = {
            "person": {
                "username": "testuser"
            }
        }
        
        self._zip_gateway.download_zip.side_effect = Exception("Zip not found")
        
        with pytest.raises(Exception) as exc_info:
            await self._download_zip_usecase.execute(get_zip_dto, current_user)

        self._zip_gateway.download_zip.assert_called_once_with(get_zip_dto, "testuser")
        assert str(exc_info.value) == "Zip not found"
        
    @pytest.mark.asyncio
    async def test_execute_unauthorized(self, setup):
        get_zip_dto = Mock()
        get_zip_dto.zip_id = "testzipid"
        
        current_user = { "person": { "username": "unauthorizeduser" } }
        
        self._zip_gateway.download_zip.side_effect = Exception("Unauthorized access")
        
        with pytest.raises(Exception) as exc_info:
            await self._download_zip_usecase.execute(get_zip_dto, current_user)

        self._zip_gateway.download_zip.assert_called_once_with(get_zip_dto, "unauthorizeduser")
        assert str(exc_info.value) == "Unauthorized access"
    
        
__all__ = ["TestDownloadZipUseCase"]

