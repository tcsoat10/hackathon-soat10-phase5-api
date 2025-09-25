
from abc import ABC, abstractmethod

from src.core.domain.dtos.register_video_dto import RegisterVideoDTO

class IFrameExtractorGateway(ABC):
    @abstractmethod
    def send_video_to_frame_extractor(self, dto: RegisterVideoDTO):
        pass

__all__ = ["IFrameExtractorGateway"]
