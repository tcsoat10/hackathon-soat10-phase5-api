import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient
from src.presentation.api.v1.middleware.auth_middleware import AuthMiddleware
from src.core.utils.jwt_util import JWTUtil
from src.core.exceptions.utils import ErrorCode
from unittest.mock import patch

fake_error = ValueError("Invalid token")
fake_error.detail = {"message": "Token inválido"}


@pytest.fixture
def app():
    app = FastAPI()

    @app.get("/api/v1/protected")
    async def protected():
        return JSONResponse(content={"message": "OK"}, status_code=200)

    app.add_middleware(AuthMiddleware)
    return app


def test_missing_authorization_header(app):
    with patch.object(JWTUtil, "decode_token", side_effect=ValueError("Invalid token")):
        client = TestClient(app)
        response = client.get("/api/v1/protected")
        assert response.status_code == 401
        assert "Missing Authorization header" in response.text


def test_invalid_token_value_error(app):
    with patch.object(JWTUtil, "decode_token", side_effect=fake_error):
        client = TestClient(app)
        response = client.get("/api/v1/protected", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
        assert ErrorCode.UNAUTHORIZED.value in response.text


def test_invalid_token_generic_exception(app):
    with patch.object(JWTUtil, "decode_token", side_effect=Exception("Unexpected error")):
        client = TestClient(app)
        response = client.get("/api/v1/protected", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 403
        assert ErrorCode.FORBIDDEN.value in response.text


def test_valid_token_sets_user_and_calls_next(app):
    with patch.object(JWTUtil, "decode_token", return_value={"username": "user123"}):
        client = TestClient(app)
        response = client.get("/api/v1/protected", headers={"Authorization": "Bearer valid_token"})
        assert response.status_code == 200
        assert response.json() == {"message": "OK"}