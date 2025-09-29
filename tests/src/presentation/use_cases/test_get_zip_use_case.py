import pytest
from unittest.mock import Mock, AsyncMock, ANY
from src.application.use_cases.get_zip_use_case import GetZipUseCase
from src.core.domain.dtos.get_zip_dto import GetZipDTO
from src.core.domain.dtos.zip_file_dto import ZipFileDTO
from src.core.domain.entities.video import Video
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.core.ports.gateways.i_zip_gateway import IZipGateway
import uuid

@pytest.fixture
def mock_video_repository():
    return Mock(spec=IVideoRepository)

@pytest.fixture
def mock_zip_gateway():
    return AsyncMock(spec=IZipGateway)

@pytest.fixture
def use_case(mock_video_repository, mock_zip_gateway):
    return GetZipUseCase(video_repository=mock_video_repository, zip_gateway=mock_zip_gateway)

@pytest.fixture
def get_zip_dto():
    return GetZipDTO(job_ref=str(uuid.uuid4()))


@pytest.fixture
def current_user():
    return {"person": {"username": "client_abc"}}


def test_build_method(mock_video_repository, mock_zip_gateway):
    use_case = GetZipUseCase.build(mock_video_repository, mock_zip_gateway)
    assert isinstance(use_case, GetZipUseCase)
    assert use_case._video_repository == mock_video_repository
    assert use_case._zip_gateway == mock_zip_gateway


@pytest.mark.asyncio
async def test_execute_success(use_case, mock_video_repository, mock_zip_gateway, get_zip_dto, current_user):
    video = Video(job_ref="job123", client_identification="client_abc", file_name="video.mp4", file_type="video/mp4")
    mock_video_repository.find_by_job_ref.return_value = video

    expected_zip = ZipFileDTO(job_ref="a8e5f6ae-7f4e-4d3b-9c1d-1234567890ab", client_identification="client_abc", file_name="frames.zip", file_url="https://storage.example.com/frames.zip", content=b"zipcontent")

    mock_zip_gateway.get_zip.return_value = expected_zip

    result = await use_case.execute(get_zip_dto, current_user)

    mock_video_repository.find_by_job_ref.assert_called_once_with(job_ref=ANY)
    mock_zip_gateway.get_zip.assert_called_once_with(get_zip_dto, "client_abc")
    assert result == expected_zip


@pytest.mark.asyncio
async def test_execute_video_not_found(use_case, mock_video_repository, get_zip_dto, current_user):
    mock_video_repository.find_by_job_ref.return_value = None

    with pytest.raises(EntityNotFoundException, match="Você não tem permissão"):
        await use_case.execute(get_zip_dto, current_user)


@pytest.mark.asyncio
async def test_execute_user_not_authorized(use_case, mock_video_repository, get_zip_dto, current_user):
    video = Video(job_ref="job123", client_identification="another_user", file_name="video.mp4", file_type="video/mp4")
    mock_video_repository.find_by_job_ref.return_value = video

    with pytest.raises(EntityNotFoundException, match="Você não tem permissão"):
        await use_case.execute(get_zip_dto, current_user)