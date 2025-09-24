
from unittest.mock import Mock
import pytest

from src.application.use_cases.sign_in_use_case import SignInUseCase
from src.core.ports.gateways.i_auth_gateway import IAuthGateway


class TestSignInUseCase:
    
    @pytest.fixture
    def setup(self):
        self._auth_gateway = Mock(spec=IAuthGateway)
        self._sign_in_usecase = SignInUseCase.build(auth_gateway=self._auth_gateway)
    
    def test_execute_success(self, setup):
        sign_in_dto = Mock()
        sign_in_dto.username = "testuser"
        sign_in_dto.password = "testpass"
        
        expected_response = {
            "access_token": "someaccesstoken",
            "token_type": "bearer",
            "expires_in": 3600
        }
        
        self._auth_gateway.sign_in.return_value = expected_response
        
        token_dto = self._sign_in_usecase.execute(sign_in_dto)
        
        self._auth_gateway.sign_in.assert_called_once_with("testuser", "testpass")
        assert token_dto.access_token == expected_response["access_token"]
        assert token_dto.token_type == expected_response["token_type"]
        
    def test_execute_failure(self, setup):
        sign_in_dto = Mock()
        sign_in_dto.username = "wronguser"
        sign_in_dto.password = "wrongpass"
        
        self._auth_gateway.sign_in.side_effect = Exception("Invalid credentials")
        
        with pytest.raises(Exception) as exc_info:
            self._sign_in_usecase.execute(sign_in_dto)

        self._auth_gateway.sign_in.assert_called_once_with("wronguser", "wrongpass")
        assert str(exc_info.value) == "Invalid credentials"
    
__all__ = ["TestSignInUseCase"]
