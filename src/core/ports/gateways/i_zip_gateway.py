from abc import ABC, abstractmethod
from src.core.domain.dtos.get_zip_dto import GetZipDTO
from src.core.domain.dtos.zip_file_dto import ZipFileDTO


class IZipGateway(ABC):
    @abstractmethod
    async def download_zip(self, get_zip_dto: GetZipDTO, client_identification: str) -> bytes:
        pass
    
    @abstractmethod
    async def get_zip(self, get_zip_dto: GetZipDTO, client_identification: str) -> ZipFileDTO:
        pass


__all__ = ["IZipGateway"]
