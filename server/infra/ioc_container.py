from dependency_injector import containers, providers
from flask_restful.reqparse import RequestParser
from domain.services import *
from .repositoriesImpl import *
from .s3_bucket import S3BUCKET
from . import S3_BUCKET, S3_ACCESS_KEY, S3_SECRET_KEY, S3_REGION_NAME


class IocContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.controllers", ".repositoriesImpl", ".message_consumer"])
    parser = providers.Factory(RequestParser)

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)

    venue_repo = providers.Factory(VenueRepository)
    venue_service = providers.Factory(VenueService, venue_repo=venue_repo)

    concert_repo = providers.Factory(ConcertRepository)
    concert_service = providers.Factory(ConcertService, concert_repo=concert_repo, venue_repo=venue_repo)

    order_repo = providers.Factory(OrderRepository)
    order_service = providers.Factory(OrderService, order_repo=order_repo, concert_repo=concert_repo)

    s3_bucket = providers.Factory(S3BUCKET,
                                bucket_name=S3_BUCKET,
                                aws_access_key_id=S3_ACCESS_KEY,
                                aws_secret_access_key=S3_SECRET_KEY,
                                region_name=S3_REGION_NAME)

