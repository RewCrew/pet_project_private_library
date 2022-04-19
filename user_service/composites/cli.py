from user_service.adapters.cli import create_cli
from user_service.composites.app_api import ConsumerMessageBus

cli = create_cli(ConsumerMessageBus)
