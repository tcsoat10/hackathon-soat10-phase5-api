import requests
import logging
from src.core.ports.gateways.i_zip_gateway import IZipGateway
from src.core.domain.dtos.get_zip_dto import GetZipDTO
from config.settings import ZIPPER_SERVICE_URL, ZIPPER_SERVICE_X_API_KEY


class ZipGateway(IZipGateway):
    def __init__(self):
        self.zip_service_url = ZIPPER_SERVICE_URL
        self.zip_service_x_api_key = ZIPPER_SERVICE_X_API_KEY
        self.logger = logging.getLogger(__name__)

    async def download_zip(self, get_zip_dto: GetZipDTO, client_identification: str) -> bytes:
        try:
            params = {
                "job_ref": get_zip_dto.job_ref,
                "client_identification": client_identification,
            }
            headers = {"x-api-key": self.zip_service_x_api_key}

            response = requests.get(
                f"{self.zip_service_url}/api/v1/zip/download",
                params=params,
                headers=headers,
                stream=True,
            )
            response.raise_for_status()

            self.logger.info(f"Successfully downloaded zip for job_ref: {get_zip_dto.job_ref}")
            return response.content
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading zip for job_ref {get_zip_dto.job_ref}: {e}")
            raise

__all__ = ["ZipGateway"]
