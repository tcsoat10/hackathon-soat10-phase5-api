
from abc import ABC, abstractmethod

class IFrameExtractorGateway(ABC):
    @abstractmethod
    def send_video_to_frame_extractor(self, video_process_result: dict):
        pass

__all__ = ["IFrameExtractorGateway"]
