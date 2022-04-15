import datetime

import pytest
from attr import asdict
from user_service.application import services, errors


@pytest.fixture(scope='function')
def user_test(users_repo, user_publisher):
    return services.UsersService(user_repo=users_repo, publisher=user_publisher)


test_data_user = {
    'id': 1,
    'name': 'TestUser',
    'email': 'TestEmail'
}

user_update = {
    'name': 'updated_name',
    'id': 1
}

wrong_user_update = {
    'name': 'updated_name',
    'id': 5
}


def test_add_user(user_test):
    user_test.add_user(**test_data_user)
    user_test.user_repo.get_or_create.assert_called_once()


def test_get_user(user_test):
    user = user_test.user_repo.get_by_id(test_data_user['id'])
    assert asdict(user) == test_data_user


def test_get_wrong_user(user_test):
    with pytest.raises(errors.ErrorUser):
        user_test.get_user(5)


def test_update_user(user_test):
    user_test.update_user(**user_update)
    user = user_test.user_repo.get_by_id(test_data_user['id'])
    assert user.name == user_update['name']


def test_update_wrong_user(user_test):
    with pytest.raises(errors.ErrorUser):
        user_test.update_user(**wrong_user_update)
