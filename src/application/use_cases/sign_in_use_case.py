from src.core.ports.gateways.i_auth_gateway import IAuthGateway
from src.core.domain.dtos.signin_dto import SignInDTO
from src.core.domain.dtos.token_dto import TokenDTO


class SignInUseCase:
    def __init__(self, auth_gateway: IAuthGateway):
        self._auth_gateway = auth_gateway

    @classmethod
    def build(cls, auth_gateway: IAuthGateway) -> "SignInUseCase":
        return cls(auth_gateway=auth_gateway)

    def execute(self, sign_in_dto: SignInDTO) -> TokenDTO:
        response_data = self._auth_gateway.sign_in(sign_in_dto.username, sign_in_dto.password)
        return TokenDTO.from_dict(response_data)

__all__ = ["SignInUseCase"]
