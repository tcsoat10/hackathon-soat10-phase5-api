
import requests
import logging
from src.core.ports.gateways.i_auth_gateway import IAuthGateway
from config.settings import AUTH_SERVICE_URL, AUTH_SERVICE_X_API_KEY


class AuthGateway(IAuthGateway):
    def __init__(self):
        self.auth_service_url = AUTH_SERVICE_URL
        self.auth_service_x_api_key = AUTH_SERVICE_X_API_KEY
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "x-api-key": self.auth_service_x_api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def sign_up(self, person_data: dict, user_data: dict) -> dict:
        self._validate_environment()

        try:
            payload = {
                "person": person_data,
                "user": user_data
            }
            response = requests.post(
                f"{self.auth_service_url}/api/v1/customers",
                json=payload,
                headers={"x-api-key": self.auth_service_x_api_key}
            )
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully signed up user")
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error signing up user: {e}")
            raise

    def sign_in(self, username: str, password: str) -> dict:
        self._validate_environment()

        try:
            payload = {
                "username": username,
                "password": password
            }
            response = requests.post(
                f"{self.auth_service_url}/api/v1/auth/token",
                data=payload,
                headers={
                    "x-api-key": self.auth_service_x_api_key,
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully signed in user: {username}")
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error signing in user: {e}")
            response_data = e.response.json()
            self.logger.error(f"Response data: {response_data}")
            if message := response_data.get('detail', {}).get('message'):
                raise ValueError(message)

            raise

    def _validate_environment(self):
        if not self.auth_service_url or not self.auth_service_x_api_key:
            raise ValueError("Auth service URL or API key is not configured.")

__all__ = ["AuthGateway"]
