from src.core.ports.gateways.i_frame_extractor_gateway import IFrameExtractorGateway
from src.core.domain.dtos.register_video_dto import RegisterVideoDTO


class SendVideoToFrameExtractorUseCase:
    def __init__(self, frame_extractor_gateway: IFrameExtractorGateway):
        self._frame_extractor_gateway = frame_extractor_gateway

    @classmethod
    def build(cls, frame_extractor_gateway: IFrameExtractorGateway) -> "SendVideoToFrameExtractorUseCase":
        return cls(frame_extractor_gateway=frame_extractor_gateway)

    def execute(self, video_dto: RegisterVideoDTO):
        return self._frame_extractor_gateway.send_video_to_frame_extractor(video_dto)