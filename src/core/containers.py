from src.core.ports.gateways.i_auth_gateway import IAuthGateway
from src.core.ports.gateways.i_notification_sender_gateway import INotificationSenderGateway
from dependency_injector import containers, providers

from config.database import get_db
from src.infrastructure.gateways.auth_gateway import AuthGateway
from src.infrastructure.gateways.notification_sender_gateway import NotificationSenderGateway
from src.core.shared.identity_map import IdentityMap
from src.infrastructure.repositories.mongoengine.video_repository import MongoVideoRepository
from src.presentation.api.v1.controllers.auth_controller import AuthController
from src.presentation.api.v1.controllers.notification_controller import NotificationController
from src.presentation.api.v1.controllers.video_controller import VideoController

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.presentation.api.v1.controllers.video_controller",
        "src.presentation.api.v1.routes.video_routes",
        "src.presentation.api.v1.controllers.auth_controller",
        "src.presentation.api.v1.routes.auth_routes",
        "src.presentation.api.v1.middleware.auth_middleware",
        "src.presentation.api.v1.controllers.notification_controller",
        "src.presentation.api.v1.routes.notification_routes",
    ])
    
    identity_map = providers.Singleton(IdentityMap)

    db_session = providers.Resource(get_db)

    video_gateway = providers.Factory(MongoVideoRepository)

    video_controller = providers.Factory(
        VideoController,
        video_repository=video_gateway        
    )
    
    notification_sender_gateway: providers.Singleton[INotificationSenderGateway] = providers.Singleton(
        NotificationSenderGateway
    )
    
    auth_gateway: providers.Factory[IAuthGateway] = providers.Factory(AuthGateway)
    auth_controller = providers.Factory(AuthController, auth_gateway=auth_gateway)

    notification_controller = providers.Factory(
        NotificationController,
        video_repository=video_gateway,
        notification_sender_gateway=notification_sender_gateway
    )
    
