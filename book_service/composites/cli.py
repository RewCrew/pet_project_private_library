import click
# from book_service.adapters.cli import loader
from book_service.composites import book_loader
# from .consumer import MessageBus

# cli = create_cli(get_books, MessageBus)
# cli = loader(get_books)

# @click.command()
# @click.argument('params', nargs=-1, type=click.UNPROCESSED)  # FIXME
# def loader(params):
#     click.echo('echo')
#     book_loader.get_books(*params)

from book_service.composites.app_api import (
    PublisherMessageBus, ConsumerMessageBus
)

from book_service.adapters.cli import create_cli

cli = create_cli(ConsumerMessageBus)
