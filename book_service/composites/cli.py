from book_service.adapters.cli import create_cli
from book_service.composites.app_api import (ConsumerMessageBus)

cli = create_cli(ConsumerMessageBus)
