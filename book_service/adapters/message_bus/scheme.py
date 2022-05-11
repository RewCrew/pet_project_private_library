from kombu import Exchange, Queue

from classic.messaging_kombu import BrokerScheme

broker_scheme = BrokerScheme(
    Queue('Queue', Exchange('Exchange')),
    Queue('BookSender', Exchange("BookExchange"))
)
