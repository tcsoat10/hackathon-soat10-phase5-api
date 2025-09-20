from src.application.use_cases.sign_up_use_case import SignUpUseCase
from src.application.use_cases.sign_in_use_case import SignInUseCase
from src.core.domain.dtos.singup_dto import SignUpDTO
from src.core.domain.dtos.signin_dto import SignInDTO
from src.core.domain.dtos.token_dto import TokenDTO
from src.core.ports.gateways.i_auth_gateway import IAuthGateway


class AuthController:
    def __init__(self, auth_gateway: IAuthGateway):
        self._auth_gateway = auth_gateway

    def sign_up(self, sign_up_dto: SignUpDTO) -> dict:
        sign_up_use_case = SignUpUseCase.build(auth_gateway=self._auth_gateway)
        return sign_up_use_case.execute(sign_up_dto)

    def sign_in(self, sign_in_dto: SignInDTO) -> TokenDTO:
        sign_in_use_case = SignInUseCase.build(auth_gateway=self._auth_gateway)
        return sign_in_use_case.execute(sign_in_dto)
