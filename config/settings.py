import os

from dotenv import load_dotenv

load_dotenv()

# Configurações de ambiente
DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, staging, production

# Configurações de servidor
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("APP_PORT", 5000))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configurações de autenticação
JWT_SECRET_KEY = os.getenv("SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

JWT_ALGORITHM = os.getenv("ALGORITHM_JWT", "HS256")

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

EMAIL_SENDER_ADDRESS = os.getenv('EMAIL_SENDER_ADDRESS')

EMAIL_HOST=os.getenv('EMAIL_HOST')
EMAIL_PORT=os.getenv('EMAIL_PORT')
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS=os.getenv('EMAIL_USE_TLS', 'true').lower() in ('true', '1')
EMAIL_USE_SSL=os.getenv('EMAIL_USE_SSL', 'false').lower() in ('true', '1')

FRAME_EXTRACTOR_SERVICE_URL = os.getenv('FRAME_EXTRACTOR_SERVICE_URL')
FRAME_EXTRACTOR_SERVICE_X_API_KEY = os.getenv('FRAME_EXTRACTOR_SERVICE_X_API_KEY')

ZIPPER_SERVICE_URL=os.getenv('ZIPPER_SERVICE_URL')
ZIPPER_SERVICE_X_API_KEY=os.getenv('ZIPPER_SERVICE_X_API_KEY')

AUTH_SERVICE_URL=os.getenv('AUTH_SERVICE_URL')
AUTH_SERVICE_X_API_KEY=os.getenv('AUTH_SERVICE_X_API_KEY')

CALLBACK_URL = os.getenv('CALLBACK_URL', 'http://localhost:8000/api/v1/notification')
API_X_API_KEY = os.getenv('API_X_API_KEY')
