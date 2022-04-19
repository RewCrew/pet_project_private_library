from kombu import Connection

from evraz.classic.messaging_kombu import KombuConsumer

from user_service.application import services

from .scheme import broker_scheme


def create_consumer(
    connection: Connection, users: services.UsersService
) -> KombuConsumer:
    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        users.message_sender,
        'BookSender',
    )

    return consumer
