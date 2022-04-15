from kombu import Connection
from sqlalchemy import create_engine

from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext

from book_service.adapters import books_api, database, message_bus
from book_service.application import services


class Settings:
    db = database.Settings()
    books_api = books_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    books_repo = database.repositories.BooksRepo(context=context)


class PublisherMessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class Application:
    books = services.BookService(
        books_repo=DB.books_repo, publisher=PublisherMessageBus.publisher
    )
    is_dev_mode = Settings.books_api.IS_DEV_MODE


class ConsumerMessageBus:
    consumer = message_bus.create_consumer(
        PublisherMessageBus.connection, Application.books
    )

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(PublisherMessageBus.connection)


class Aspects:
    services.join_points.join(DB.context)
    books_api.join_points.join(PublisherMessageBus.publisher, DB.context)


app = books_api.create_app(
    books=Application.books, is_dev_mode=Application.is_dev_mode
)

if __name__ == "__main__":
    from wsgiref import simple_server

    with simple_server.make_server('', 8000, app=app) as server:
        server.serve_forever()

        # hupper - m
        # waitress - -port = 8000 - -host = 127.0
        # .0
        # .1
        # user_service.composites.users_api: app
