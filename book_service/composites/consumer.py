# from threading import Thread
#
# from sqlalchemy import create_engine
#
# from evraz.classic.sql_storage import TransactionContext
#
# from book_service.adapters import database, books_api, message_bus
# from book_service.application import services
#
# from kombu import Connection
#
#
#
# class Settings:
#     db = database.Settings()
#     books_api = books_api.Settings()
#     message_bus = message_bus.Settings()
#
#
# class DB:
#     engine = create_engine(Settings.db.DB_URL)
#     database.metadata.create_all(engine)
#
#     context = TransactionContext(bind=engine)
#
#     books_repo = database.repositories.BooksRepo(context=context)
#
# #
# class Application:
#     book_controller = services.BookService(books_repo=DB.books_repo)
#     is_dev_mode = Settings.books_api.IS_DEV_MODE
#
# #
# class MessageBus:
#     connection = Connection(Settings.message_bus.BROKER_URL)
#
#     message_bus.broker_scheme.declare(connection)
#     consumer = message_bus.create_consumer(connection, Application.book_controller)
#
# #
# class Application:
#     is_dev_mode = Settings.books_api.IS_DEV_MODE
#     books = services.BookService(books_repo=DB.books_repo,
#                               # publisher=MessageBus.publisher,
#                              )
#
#
# class MessageBus:
#     connection = Connection(Settings.message_bus.BROKER_URL)
#     consumer = message_bus.create_consumer(connection, Application.books)
#
#     @staticmethod
#     def declare_scheme():
#         message_bus.broker_scheme.declare(MessageBus.connection)
#
#
# class Aspects:
#     services.join_points.join(DB.context)
#     books_api.join_points.join(DB.context)
#
#
# MessageBus.declare_scheme()
# consumer = Thread(target=MessageBus.consumer.run, daemon=True)
# consumer.start()
