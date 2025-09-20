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

'''
# Listar vídeos do usuário
@router.get(
    "/videos",
    response_model=List[VideoDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_LIST_VIDEOS])],
)
@inject
async def list_videos(
    status: Optional[List[str]] = Query(
        default=[],
        description=f"Lista de status dos vídeos para filtrar. Valores válidos: {', '.join([str(s.status) for s in VideoStatusEnum])}"
    ),
    search: Optional[str] = Query(
        default=None,
        description="Buscar por nome do arquivo"
    ),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Lista os vídeos do usuário autenticado com filtros opcionais
    """
    return await controller.list_videos(status, search, skip, limit, current_user)

# Obter detalhes de um vídeo
@router.get(
    "/videos/{video_id}",
    response_model=VideoDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_VIEW_VIDEO])],
)
@inject
async def get_video_by_id(
    video_id: str,
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Obtém detalhes de um vídeo específico
    """
    return await controller.get_video_by_id(video_id, current_user)

# Deletar vídeo
@router.delete(
    "/videos/{video_id}",
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_DELETE_VIDEO])],
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_video(
    video_id: str,
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Remove um vídeo e seus arquivos associados
    """
    await controller.delete_video(video_id, current_user)
    return {"detail": "Vídeo deletado com sucesso."}

# Download do ZIP com frames
@router.get(
    "/videos/{video_id}/download",
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_DOWNLOAD_FRAMES])],
    status_code=status.HTTP_200_OK,
)
@inject
async def download_frames(
    video_id: str,
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Download do arquivo ZIP com os frames extraídos
    """
    return await controller.download_frames(video_id, current_user)

# Reprocessar vídeo
@router.post(
    "/videos/{video_id}/reprocess",
    response_model=VideoDTO,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_REPROCESS_VIDEO])],
    status_code=status.HTTP_200_OK,
)
@inject
async def reprocess_video(
    video_id: str,
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Reprocessa um vídeo que falhou ou precisa ser processado novamente
    """
    return await controller.reprocess_video(video_id, current_user)

# Cancelar processamento de vídeo
@router.post(
    "/videos/{video_id}/cancel",
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_CANCEL_PROCESSING])],
    status_code=status.HTTP_200_OK,
)
@inject
async def cancel_video_processing(
    video_id: str,
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Cancela o processamento de um vídeo
    """
    await controller.cancel_processing(video_id, current_user)
    return {"detail": "Processamento cancelado com sucesso."}

# Obter status do job de processamento
@router.get(
    "/videos/{video_id}/job/status",
    response_model=JobStatusDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_VIEW_JOB_STATUS])],
)
@inject
async def get_job_status(
    video_id: str,
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Consulta o status de processamento de um vídeo
    """
    return await controller.get_job_status(video_id, current_user)

# Listar jobs de processamento
@router.get(
    "/videos/{video_id}/jobs",
    response_model=List[JobDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_LIST_JOBS])],
)
@inject
async def list_video_jobs(
    video_id: str,
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Lista todos os jobs de processamento de um vídeo
    """
    return await controller.list_video_jobs(video_id, current_user)

# Listar todos os jobs do usuário
@router.get(
    "/jobs",
    response_model=List[JobDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_LIST_ALL_JOBS])],
)
@inject
async def list_user_jobs(
    status: Optional[List[str]] = Query(
        default=[],
        description="Lista de status dos jobs para filtrar (pending, processing, completed, failed)"
    ),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Lista todos os jobs de processamento do usuário
    """
    return await controller.list_user_jobs(status, skip, limit, current_user)

# Obter job específico por ID
@router.get(
    "/jobs/{job_id}",
    response_model=JobDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[VideoPermissions.CAN_VIEW_JOB])],
)
@inject
async def get_job_by_id(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    """
    Obtém detalhes de um job específico
    """
    return await controller.get_job_by_id(job_id, current_user)
'''