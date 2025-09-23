from abc import ABC, abstractmethod
from src.core.domain.dtos.get_zip_dto import GetZipDTO


class IZipGateway(ABC):
    @abstractmethod
    async def download_zip(self, get_zip_dto: GetZipDTO, client_identification: str) -> bytes:
        pass

__all__ = ["IZipGateway"]
