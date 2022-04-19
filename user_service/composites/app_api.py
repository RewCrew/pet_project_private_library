from kombu import Connection
from sqlalchemy import create_engine

from evraz.classic.sql_storage import TransactionContext

from user_service.adapters import database, users_api, message_bus
from user_service.application import services


class Settings:
    db = database.Settings()
    chat_api = users_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    users_repo = database.repositories.UsersRepo(context=context)


class Application:
    register = services.UsersService(user_repo=DB.users_repo)
    is_dev_mode = Settings.chat_api.IS_DEV_MODE


class ConsumerMessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    consumer = message_bus.create_consumer(connection, Application.register)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(ConsumerMessageBus.connection)


class Aspects:
    services.join_points.join(DB.context)
    users_api.join_points.join(DB.context)


app = users_api.create_app(
    register=Application.register, is_dev_mode=Application.is_dev_mode
)

if __name__ == "__main__":
    from wsgiref import simple_server

    with simple_server.make_server('0.0.0.0', 1234, app=app) as server:
        server.serve_forever()

        # hupper - m
        # waitress - -port = 8000 - -host = 127.0
        # .0
        # .1
        # user_service.composites.users_api: app
