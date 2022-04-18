from unittest.mock import Mock

import pytest

from book_service.adapters import books_api
from falcon import testing
from book_service.application import services


@pytest.fixture(scope='function')
def books_service():
    service = Mock(services.BookService)

    return service




@pytest.fixture(scope='function')
def client(
    books_service
):
    app = books_api.create_app(
        is_dev_mode=True,
        books=books_service,
    )

    return testing.TestClient(app)