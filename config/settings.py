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

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')

BOTO_MAX_ATTEMPTS = int(os.getenv('BOTO_MAX_ATTEMPTS', 10))
EMAIL_SENDER_ADDRESS = os.getenv('EMAIL_SENDER_ADDRESS')
