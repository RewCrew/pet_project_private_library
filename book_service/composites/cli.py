import click

from book_service.adapters.cli import create_cli

# from book_service.adapters.cli import loader
from book_service.composites import book_loader
from book_service.composites.app_api import (
    ConsumerMessageBus,
    PublisherMessageBus,
)

# from .consumer import MessageBus

# cli = create_cli(get_books, MessageBus)
# cli = loader(get_books)

# @click.command()
# @click.argument('params', nargs=-1, type=click.UNPROCESSED)  # FIXME
# def loader(params):
#     click.echo('echo')
#     book_loader.get_books(*params)



cli = create_cli(ConsumerMessageBus)
