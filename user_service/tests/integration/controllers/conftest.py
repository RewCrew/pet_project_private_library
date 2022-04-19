from unittest.mock import Mock

import pytest

from user_service.adapters import users_api
from falcon import testing
from user_service.application import services

@pytest.fixture(scope='function')
def users_service():
    service = Mock(services.UsersService)

    return service




@pytest.fixture(scope='function')
def client(
    users_service
):
    app = users_api.create_app(
        is_dev_mode=True,
        register=users_service,
    )

    return testing.TestClient(app)