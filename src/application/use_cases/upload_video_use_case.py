import uuid
import httpx
from datetime import datetime
from typing import Dict, Any
from fastapi import UploadFile, HTTPException, status

from src.core.domain.entities.video import Video
from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.core.domain.dtos.video_dto import VideoDTO
from src.core.constants.video_status import VideoStatusEnum
from src.application.use_cases.send_video_to_frame_extractor_use_case import SendVideoToFrameExtractorUseCase
from src.core.domain.dtos.register_video_dto import RegisterVideoDTO
from src.infrastructure.gateways.frame_extractor_gateway import FrameExtractorGateway


class UploadVideoUseCase:
    def __init__(
        self,
        video_repository: IVideoRepository,        
    ):
        self.video_repository = video_repository        
    
    @classmethod
    def build(cls, video_repository: IVideoRepository) -> "UploadVideoUseCase":
        return cls(video_repository=video_repository)

    async def execute(self, file: UploadFile, current_user: Dict[str, Any] = {}) -> VideoDTO:        
        #self._validate_file(file)           
        
        register_video_dto = RegisterVideoDTO(
            video_file=file,
            client_identification='test-user',
            notify_url="http://localhost:3000/"
        )
        send_to_frame_extraction_use_case = SendVideoToFrameExtractorUseCase.build(
            frame_extractor_gateway=FrameExtractorGateway()
        )
        video_response = send_to_frame_extraction_use_case.execute(video_dto=register_video_dto)
        video = Video(
            client_identification=register_video_dto.client_identification,
            status=VideoStatusEnum.PENDING_FRAMES.status,
            job_ref=video_response['job_ref']
        )
        video = self.video_repository.save(video)
        return VideoDTO.from_entity(video)

    def _validate_file(self, file: UploadFile) -> None:                
        allowed_types = ["video/mp4", "video/avi", "video/mov"]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não suportado. Tipos aceitos: {', '.join(allowed_types)}"
            )
        
        # Validar nome do arquivo
        if not file.filename or len(file.filename) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome do arquivo inválido"
            )

    