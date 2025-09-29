import pytest
from unittest.mock import Mock
from src.application.use_cases.sign_up_use_case import SignUpUseCase
from src.core.domain.dtos.singup_dto import SignUpDTO
from src.core.domain.dtos.singup_dto import PersonDTO
from src.core.domain.dtos.singup_dto import UserDTO

@pytest.fixture
def valid_signup_dto():
    person = PersonDTO(name="João", cpf="123.456.789-00", email="joao@exemplo.com", birth_date="1990-01-01")
    user = UserDTO(name="João", password="securepass")
    return SignUpDTO(person=person, user=user)

@pytest.fixture
def mock_gateway():
    gateway = Mock()
    gateway.sign_up.return_value = {"status": "success", "job_id": "abc123"}
    return gateway

def test_build_method(mock_gateway):
    usecase = SignUpUseCase.build(auth_gateway=mock_gateway)
    assert isinstance(usecase, SignUpUseCase)

def test_execute_success(valid_signup_dto, mock_gateway):
    usecase = SignUpUseCase(mock_gateway)
    result = usecase.execute(valid_signup_dto)

    expected_person = {"name": "João", "cpf": "12345678900", "email":"joao@exemplo.com", "birth_date":"1990-01-01"}  # CPF sem pontuação
    expected_user = {"name": "João", "password": "securepass"}

    mock_gateway.sign_up.assert_called_once_with(expected_person, expected_user)
    assert result["status"] == "success"
    assert result["job_id"] == "abc123"

def test_execute_gateway_failure(valid_signup_dto):
    gateway = Mock()
    gateway.sign_up.side_effect = Exception("Erro no serviço externo")

    usecase = SignUpUseCase(gateway)

    with pytest.raises(Exception) as exc_info:
        usecase.execute(valid_signup_dto)

    assert str(exc_info.value) == "Erro no serviço externo"