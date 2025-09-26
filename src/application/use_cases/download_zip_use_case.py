import requests
from src.core.ports.gateways.i_zip_gateway import IZipGateway
from src.core.domain.dtos.get_zip_dto import GetZipDTO


class DownloadZipUseCase:
    def __init__(self, zip_gateway: IZipGateway):
        self._zip_gateway = zip_gateway

    @classmethod
    def build(cls, zip_gateway: IZipGateway) -> "DownloadZipUseCase":
        return cls(zip_gateway=zip_gateway)

    async def execute(self, get_zip_dto: GetZipDTO, current_user: dict) -> bytes:        
        zip_file = await self._zip_gateway.get_zip(get_zip_dto, current_user['person']['username'])
        zip_content = requests.get(zip_file.file_url)
        return zip_content.content


__all__ = ["DownloadZipUseCase"]
