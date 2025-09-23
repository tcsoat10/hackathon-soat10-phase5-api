from fastapi import APIRouter, Depends, Security, status, UploadFile, File
from dependency_injector.wiring import inject, Provide

from src.core.auth.dependencies import get_current_user
from src.core.constants.permissions import VideoPermissions
from src.presentation.api.v1.controllers.video_controller import VideoController
from src.core.domain.dtos.video_dto import VideoDTO
from src.core.containers import Container

router = APIRouter()

@router.post(
    "/videos",
    response_model=VideoDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_SEND_VIDEO])],
)
@inject
async def upload_video(
    file: UploadFile = File(..., description="Arquivo de vídeo para processamento"),
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Faz upload de um vídeo para extração de frames
    """
    return await controller.upload_video(file, current_user=current_user)

@router.get(
    "/videos",
    response_model=list[VideoDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_VIEW_VIDEO])],
)
@inject
async def list_videos(
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Lista todos os vídeos enviados pelo usuário autenticado
    """
    return await controller.list_videos(current_user=current_user)
