from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.presentation.api.v1.controllers.auth_controller import AuthController
from src.core.domain.dtos.singup_dto import SignUpDTO
from src.core.domain.dtos.signin_dto import SignInDTO
from src.core.domain.dtos.token_dto import TokenDTO

router = APIRouter(prefix="/auth")


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=dict
)
@inject
def sign_up(
    sign_up_dto: SignUpDTO,
    controller: AuthController = Depends(Provide[Container.auth_controller]),
):
    """
    Registers a new user in the system.
    """
    return controller.sign_up(sign_up_dto)


@router.post(
    "/signin",
    status_code=status.HTTP_200_OK,
    response_model=TokenDTO
)
@inject
def sign_in(
    sign_in_dto: SignInDTO,
    controller: AuthController = Depends(Provide[Container.auth_controller]),
):
    """
    Authenticates a user and returns an access token.
    """
    return controller.sign_in(sign_in_dto)
