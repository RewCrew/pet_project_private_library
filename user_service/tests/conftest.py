import pytest
from unittest.mock import Mock

from evraz.classic.messaging import Publisher
from user_service.application import interfaces, dataclasses


@pytest.fixture(scope='function')
def user():
    return dataclasses.User(
        id=1,
        name='TestUser',
        email='TestEmail'
    )


@pytest.fixture(scope='function')
def users_repo(user):
    users_repo = Mock(interfaces.UsersRepo)
    users_repo.get_or_create = Mock(return_value=user)
    users_repo.get_by_id = Mock(return_value=user)
    users_repo.update_user = Mock(return_value=user)
    return users_repo


@pytest.fixture(scope='function')
def user_publisher():
    user_publisher = Mock(Publisher)
    user_publisher.plan = Mock(return_value=None)
    return user_publisher
