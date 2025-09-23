from fastapi.responses import StreamingResponse
from src.core.ports.gateways.i_zip_gateway import IZipGateway
from src.core.domain.dtos.get_zip_dto import GetZipDTO
from src.application.use_cases.download_zip_use_case import DownloadZipUseCase


class ZipController:
    def __init__(self, zip_gateway: IZipGateway):
        self._zip_gateway = zip_gateway

    async def download_zip(self, get_zip_dto: GetZipDTO, current_user: dict) -> bytes:
        download_zip_use_case = DownloadZipUseCase.build(zip_gateway=self._zip_gateway)
        file_content = await download_zip_use_case.execute(get_zip_dto, current_user)
        return StreamingResponse(
            content=iter([file_content]),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={get_zip_dto.job_ref}.zip"}
        )

__all__ = ["ZipController"]

