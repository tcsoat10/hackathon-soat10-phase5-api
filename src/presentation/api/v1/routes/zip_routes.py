from fastapi import APIRouter, Depends, Security, status
from dependency_injector.wiring import inject, Provide

from src.core.auth.dependencies import get_current_user
from src.core.constants.permissions import ZipPermissions
from src.presentation.api.v1.controllers.zip_controller import ZipController
from src.core.domain.dtos.get_zip_dto import GetZipDTO
from src.core.containers import Container

router = APIRouter()

@router.get(
    "/zip/download",
    response_model=None,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ZipPermissions.CAN_DOWNLOAD_ZIP])],
)
@inject
async def download_zip(
    get_zip_dto: GetZipDTO = Depends(),
    current_user: dict = Depends(get_current_user),
    controller: ZipController = Depends(Provide[Container.zip_controller]),
):
    """
    Faz download de um arquivo ZIP de frames de vídeo.
    """
    return await controller.download_zip(get_zip_dto, current_user=current_user)