import pytest
from sqlalchemy import create_engine
from book_service.adapters.database import Settings
from evraz.classic.sql_storage import TransactionContext

from book_service.adapters.database.tables import metadata


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(Settings().DB_URL)

    for key, value in metadata.tables.items():
        value.schema = None

    metadata.create_all(engine)

    return engine


@pytest.fixture(scope='session')
def transaction_context(engine):
    return TransactionContext(bind=engine)


@pytest.fixture(scope='function')
def session(transaction_context: TransactionContext):
    session = transaction_context.current_session

    if session.in_transaction():
        session.begin_nested()
    else:
        session.begin()

    yield session

    session.rollback()
