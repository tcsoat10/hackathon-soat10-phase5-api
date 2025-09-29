from src.core.domain.entities.video import Video
from src.core.ports.gateways.i_zip_gateway import IZipGateway
from src.core.ports.repositories.i_video_repository import IVideoRepository
from src.core.ports.gateways.i_notification_sender_gateway import INotificationSenderGateway
from src.core.domain.dtos.notification_dto import NotificationDTO
from src.core.constants.video_status import VideoStatusEnum
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
import logging


class NotificationController:
    def __init__(
        self,
        video_repository: IVideoRepository,
        zip_gateway: IZipGateway,
        notification_sender_gateway: INotificationSenderGateway
    ):
        self._video_repository: IVideoRepository = video_repository
        self._notification_sender_gateway: INotificationSenderGateway = notification_sender_gateway
        self._zip_gateway: IZipGateway = zip_gateway
        self.logger = logging.getLogger(__name__)

    async def handle_notification(self, notification_dto: NotificationDTO):
        self.logger.info(f"Received notification for job_ref: {notification_dto.job_ref}")

        video: Video = self._video_repository.find_by_job_ref(notification_dto.job_ref)
        if not video:
            raise EntityNotFoundException(f"Video with job_ref {notification_dto.job_ref} not found.")

        mapped_status = self._map_status(notification_dto.status, notification_dto.service)
        print(f"Selected Status: {mapped_status}")

        if (
            video.status == "N/A" or
            VideoStatusEnum.get_by_status(video.status).order < VideoStatusEnum.get_by_status(mapped_status).order
        ):
            video.status = mapped_status
        
        video.updated_at = notification_dto.timestamp
        video = self._video_repository.save(video)

        self.logger.info(f"Video {video.id} status updated to {video.status}")
        
        print(notification_dto.model_dump())

        if video.status in [VideoStatusEnum.COMPLETED.status, VideoStatusEnum.ERROR.status]:
            self.logger.info(f"Sending completion email for video {video.id}")
            
            is_completed = video.status == VideoStatusEnum.COMPLETED.status
            recipient_email = video.email
            subject = "Seu vídeo foi processado com sucesso!" if is_completed else "Houve um erro no processamento do seu vídeo"

            if is_completed:
                message = (
                    f"O processamento do seu vídeo (Job Ref: {video.job_ref}) foi concluído com sucesso. "
                    f"Acesse seu painel para baixar o arquivo ZIP."
                )
            else:
                detail = getattr(notification_dto, "detail", None) or "Sem detalhes disponíveis"
                message = (
                    f"Ocorreu um erro durante o processamento do seu vídeo (Job Ref: {video.job_ref}). "
                    f"Detalhes: {detail}"
                )
            
            email_data = {
                "username": video.client_identification,
                "message": message,
                "link_download": notification_dto.zip_url
            }
            
            self._notification_sender_gateway.send_email(recipient_email, subject, email_data)

    def _map_status(self, status: str, service: str) -> VideoStatusEnum:
        video_status = {
            "frame_extractor": {
                "PENDING": VideoStatusEnum.PENDING_FRAMES.status,
                "QUEUED": VideoStatusEnum.QUEUED_FRAMES.status,
                "PROCESSING": VideoStatusEnum.PROCESSING_FRAMES.status,
                "COMPLETED": VideoStatusEnum.PENDING_ZIP.status,
                "ERROR": VideoStatusEnum.ERROR.status,
            },
            "zip_service": {
                "PENDING": VideoStatusEnum.PENDING_ZIP.status,
                "QUEUED": VideoStatusEnum.QUEUED_ZIP.status,
                "PROCESSING": VideoStatusEnum.PROCESSING_ZIP.status,
                "COMPLETED": VideoStatusEnum.COMPLETED.status,
                "ERROR": VideoStatusEnum.ERROR.status,
            }
        }
        
        return video_status.get(service, {}).get(status.upper(), "N/A")
        