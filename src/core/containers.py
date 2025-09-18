from dependency_injector import containers, providers

from config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.infrastructure.repositories.mongoengine.video_repository import VideoRepository
from src.infrastructure.gateways.object_storage_gateway import ObjectStorageGateway
from src.presentation.api.v1.controllers.video_controller import VideoController

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.presentation.api.v1.controllers.video_controller",
        "src.presentation.api.v1.routes.video_routes"        
    ])
    
    identity_map = providers.Singleton(IdentityMap)

    db_session = providers.Resource(get_db)

    storage_gateway = providers.Singleton(ObjectStorageGateway)
    video_gateway = providers.Factory(VideoRepository, db_session=db_session, identity_map=identity_map)

    video_controller = providers.Factory(
        VideoController,
        video_repository=video_gateway,
        storage_gateway=storage_gateway
    )
