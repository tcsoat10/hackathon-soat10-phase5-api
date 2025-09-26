from src.core.domain.dtos.zip_file_dto import ZipFileDTO
from src.core.domain.entities.video import Video
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.gateways.i_zip_gateway import IZipGateway
from src.core.domain.dtos.get_zip_dto import GetZipDTO
from src.core.ports.repositories.i_video_repository import IVideoRepository


class GetZipUseCase:
    def __init__(self, video_repository: IVideoRepository, zip_gateway: IZipGateway):
        self._video_repository: IVideoRepository = video_repository
        self._zip_gateway = zip_gateway

    @classmethod
    def build(cls, video_repository: IVideoRepository, zip_gateway: IZipGateway) -> "GetZipUseCase":
        return cls(video_repository=video_repository, zip_gateway=zip_gateway)

    async def execute(self, get_zip_dto: GetZipDTO, current_user: dict) -> ZipFileDTO:
        video: Video = self._video_repository.find_by_job_ref(job_ref=get_zip_dto.job_ref)
        if not video or video.client_identification != current_user['person']['username']:
            raise EntityNotFoundException(message="Você não tem permissão para acessar este arquivo.")
        
        return await self._zip_gateway.get_zip(get_zip_dto, current_user['person']['username'])

__all__ = ["GetZipUseCase"]
