from kombu import Connection

from classic.messaging_kombu import KombuConsumer

from book_service.application import services

from .scheme import broker_scheme


def create_consumer(
    connection: Connection, books: services.BookService
) -> KombuConsumer:
    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        books.add_book,
        'Queue',
    )

    return consumer
