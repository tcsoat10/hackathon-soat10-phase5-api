import uuid
import httpx
from datetime import datetime
from typing import Dict, Any
from fastapi import UploadFile, HTTPException, status

from src.core.domain.entities.video import Video
from src.core.domain.repositories.i_video_repository import IVideoRepository
from src.core.domain.entities.storage_item import StorageItem
from src.core.domain.entities.storage_object import StorageObject
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.core.domain.dtos.video.video_dto import VideoDTO
from src.constants.video_status import VideoStatus
from src.application.use_cases.send_video_to_frame_extractor_use_case import SendVideoToFrameExtractorUseCase
from src.core.domain.dtos.register_video_dto import RegisterVideoDTO
from src.infrastructure.gateways.frame_extractor_gateway import FrameExtractorGateway


class UploadVideoUseCase:
    def __init__(
        self,
        video_repository: IVideoRepository,
        storage_gateway: ObjectStorageGateway
    ):
        self.video_repository = video_repository
        self.storage_gateway = storage_gateway
    
    @classmethod
    def build(cls, video_repository: IVideoRepository, storage_gateway: ObjectStorageGateway) -> "UploadVideoUseCase":
        return cls(video_repository=video_repository, storage_gateway=storage_gateway)

    async def execute(self, file: UploadFile, current_user: Dict[str, Any]) -> VideoDTO:        
        self._validate_file(file)   
        
        storage_object = await self._upload_to_s3(file, file.filename)
        
        video = Video(            
            client_identification=current_user["id"],
            bucket=storage_object.bucket,
            video_path=storage_object.key,
            notification_url="http://localhost:3000/"
        )        
        
        saved_video = self.video_repository.save(video)        
        
        register_video_dto = RegisterVideoDTO(
            video_file=file,
            client_identification=current_user["id"],
            notify_url="http://localhost:3000/"
        )
        send_to_frame_extraction_use_case = SendVideoToFrameExtractorUseCase.build(
            frame_extractor_gateway=FrameExtractorGateway()
        )
        send_to_frame_extraction_use_case.execute(video_dto=register_video_dto)        
        return VideoDTO.from_entity(saved_video)

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

    async def _upload_to_s3(self, file: UploadFile, video_id: str) -> 'StorageObject':        
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'mp4'
        s3_key = f"videos/{video_id}.{file_extension}"
        
        await file.seek(0)
        file_content = await file.read()
        
        storage_item = StorageItem(
            bucket="video-frame-extractor-hackathon",
            key=s3_key,
            content=file_content,
            content_type=file.content_type
        )
        
        storage_object = self.storage_gateway.upload_object(storage_item)
        
        return storage_object    