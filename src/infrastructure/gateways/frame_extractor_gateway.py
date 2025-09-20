import requests
import logging
from src.core.ports.gateways.i_frame_extractor_gateway import IFrameExtractorGateway
from src.config.settings import FRAME_EXTRACTOR_SERVICE_URL, FRAME_EXTRACTOR_SERVICE_X_API_KEY
from src.core.domain.dtos.register_video_dto import RegisterVideoDTO

class FrameExtractorGateway(IFrameExtractorGateway):
    def __init__(self):
        self.frame_extractor_service_url = FRAME_EXTRACTOR_SERVICE_URL
        self.frame_extractor_service_x_api_key = FRAME_EXTRACTOR_SERVICE_X_API_KEY
        self.logger = logging.getLogger(__name__)

    def send_video_to_frame_extractor(self, dto: RegisterVideoDTO):
        try:
            payload = {
                'client_identification': dto.client_identification,
                'notify_url': dto.notify_url
            }
            video_dict = {
                'video_file': (dto.video_file.filename, dto.video_file.file, dto.video_file.content_type)
            }
            response = requests.post(
                f"{self.frame_extractor_service_url}/api/v1/video/register",
                params=payload,
                files=video_dict,
                headers={"x-api-key": self.frame_extractor_service_x_api_key}
            )
            
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully sent video process result to Frame Extractor Service: {data['job_ref']}")
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending video process result to Frame Extractor Service: {e}")
            raise

__all__ = ["FrameExtractorGateway"]
