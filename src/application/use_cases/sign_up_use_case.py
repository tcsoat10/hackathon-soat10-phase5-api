from src.core.ports.gateways.i_auth_gateway import IAuthGateway
from src.core.domain.dtos.singup_dto import SignUpDTO


class SignUpUseCase:
    def __init__(self, auth_gateway: IAuthGateway):
        self._auth_gateway: IAuthGateway = auth_gateway

    @classmethod
    def build(cls, auth_gateway: IAuthGateway) -> "SignUpUseCase":
        return cls(auth_gateway=auth_gateway)

    def execute(self, sign_up_dto: SignUpDTO) -> dict:
        person_data = sign_up_dto.person.model_dump()
        user_data = sign_up_dto.user.model_dump()
        
        person_data['cpf'] = person_data['cpf'].replace('.', '').replace('-', '')
        
        return self._auth_gateway.sign_up(person_data, user_data)

__all__ = ["SignUpUseCase"]
