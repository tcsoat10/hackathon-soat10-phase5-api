from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.presentation.api.v1.controllers.notification_controller import NotificationController
from src.core.domain.dtos.notification_dto import NotificationDTO

router = APIRouter()

@router.post(
    "/notification",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Recebe notificações de serviços externos",
    description="Endpoint para receber notificações de outros serviços, como o extrator de frames, sobre o status de processamento de vídeos."
)
@inject
async def receive_notification(
    notification_dto: NotificationDTO,
    controller: NotificationController = Depends(Provide[Container.notification_controller]),
):
    """
    Recebe uma notificação de um serviço externo.
    """
    await controller.handle_notification(notification_dto)
    return {"message": "Notification received successfully"}
