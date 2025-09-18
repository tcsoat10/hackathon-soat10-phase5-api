import requests
import logging
from src.core.ports.gateways.i_frame_extractor_gateway import IFrameExtractorGateway
from src.config.settings import FRAME_EXTRACTOR_SERVICE_URL, FRAME_EXTRACTOR_SERVICE_X_API_KEY

class FrameExtractorGateway(IFrameExtractorGateway):
    def __init__(self):
        self.frame_extractor_service_url = FRAME_EXTRACTOR_SERVICE_URL
        self.frame_extractor_service_x_api_key = FRAME_EXTRACTOR_SERVICE_X_API_KEY
        self.logger = logging.getLogger(__name__)

    def send_video_to_frame_extractor(self, video_process_result: dict):
        try:
            response = requests.post(
                f"{self.frame_extractor_service_url}/api/v1/video/register",
                json=video_process_result,
                headers={"x-api-key": self.zipper_service_x_api_key}
            )
            response.raise_for_status()
            self.logger.info(f"Successfully sent video process result to Zipper Service: {video_process_result.get('job_ref')}")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error sending video process result to Zipper Service: {e}")
            raise

__all__ = ["ZipperServiceGateway"]
