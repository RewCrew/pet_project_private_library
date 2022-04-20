import pytest
from attr import asdict

from user_service.adapters.database import tables
from user_service.adapters.database.repositories import UsersRepo


@pytest.fixture(scope='function')
def fill_db(session, user, user2):
    users_data = [asdict(user), asdict(user2)]
    session.execute(tables.users.insert(), users_data)


@pytest.fixture(scope='function')
def users_repo(transaction_context):
    return UsersRepo(context=transaction_context)


def test_add_user(users_repo, user):
    result = users_repo.add(user)
    assert result == user


def test_get_by_id(users_repo, fill_db, user):
    result = users_repo.get_by_id(id_=1)
    assert result == user


def test_get_all(users_repo, user, user2, fill_db):
    result = users_repo.get_all()
    assert result == [user, user2]


if __name__ == '__main__':
    pytest.main()