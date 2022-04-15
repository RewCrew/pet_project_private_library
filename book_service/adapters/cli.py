import click

from book_service.composites import book_loader

# def create_cli(get_books, MessageBus):

# @click.command()
# @click.argument('params', nargs=-1, type=click.UNPROCESSED)  # FIXME
# def loader(params):
#     click.echo('echo')
#     book_loader.get_books(*params)

#
# def create_cli(get_books):
#
#     @click.group()
#     def cli():
#         pass
#
#     # @cli.command()
#     # @click.argument('alembic_args', nargs=-1, type=click.UNPROCESSED)
#     # def alembic(alembic_args):
#     #     alembic_run_cmd(*alembic_args)
#
#     @cli.command()
#     @click.argument('params', nargs=-1, type=click.UNPROCESSED) #FIXME
#     def loader(params):
#         get_books(*params)
#

# return cli


def create_cli(MessageBus):

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('params', nargs=-1, type=click.UNPROCESSED)
    def get_books(params: list):
        click.echo('echo2')
        click.echo(params)
        books = book_loader.get_books(params)

        return books

    @cli.command()
    def consumer():
        click.echo('oks')
        MessageBus.declare_scheme()
        click.echo('aaa')
        MessageBus.consumer.run()

    return cli
