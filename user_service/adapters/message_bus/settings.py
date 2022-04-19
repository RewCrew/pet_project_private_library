import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    BROKER_URL: str = f'amqp://' \
                      f'{os.getenv("RABBITMQ_USER", "superuser")}:' \
                      f'{os.getenv("RABBITMQ_PASS", "password")}@' \
                      f'{os.getenv("RABBITMQ_HOST", "127.0.0.1")}:' \
                      f'{os.getenv("RABBITMQ_PORT", "5672")}'

    LOGGING_LEVEL: str = 'INFO'

    @property
    def LOGGING_CONFIG(self):
        return {
            'loggers': {
                'kombu': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }
