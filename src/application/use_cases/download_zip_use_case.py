from src.core.ports.gateways.i_zip_gateway import IZipGateway
from src.core.domain.dtos.get_zip_dto import GetZipDTO


class DownloadZipUseCase:
    def __init__(self, zip_gateway: IZipGateway):
        self._zip_gateway = zip_gateway

    @classmethod
    def build(cls, zip_gateway: IZipGateway) -> "DownloadZipUseCase":
        return cls(zip_gateway=zip_gateway)

    async def execute(self, get_zip_dto: GetZipDTO, current_user: dict) -> bytes:
        return await self._zip_gateway.download_zip(get_zip_dto, current_user['person']['username'])

__all__ = ["DownloadZipUseCase"]
