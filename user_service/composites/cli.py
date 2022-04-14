
from user_service.composites.app_api import (
ConsumerMessageBus)

from user_service.adapters.cli import create_cli

cli = create_cli(ConsumerMessageBus)