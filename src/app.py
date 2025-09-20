from fastapi import FastAPI
from config.custom_openapi import custom_openapi
from src.presentation.api.v1.middleware.identity_map_middleware import IdentityMapMiddleware
from src.core.containers import Container
from src.presentation.api.v1.middleware.auth_middleware import AuthMiddleware
from src.presentation.api.v1.middleware.custom_error_middleware import CustomErrorMiddleware
from src.presentation.api.v1.routes.health_check import router as health_check_router
from src.presentation.api.v1.routes.video_routes import router as video_router
from contextlib import asynccontextmanager
from config.database import connect_db, disconnect_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_db()
    yield
    disconnect_db()

app = FastAPI(
    title="Main API - FIAP",
    lifespan=lifespan,
    description="",
    version="0.1.0",    
)


# Inicializando o container de dependências
container = Container()
app.container = container

app.openapi = lambda: custom_openapi(app)

app.add_middleware(CustomErrorMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(IdentityMapMiddleware)

PREFIX_API_V1 = "/api/v1"

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix=PREFIX_API_V1)
app.include_router(video_router, prefix=PREFIX_API_V1)
