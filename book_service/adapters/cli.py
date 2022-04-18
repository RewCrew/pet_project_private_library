import click

from book_service.composites import book_loader


def create_cli(MessageBus):

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('params', nargs=-1, type=click.UNPROCESSED)
    def get_books(params: list):
        # click.echo('echo2')
        click.echo(params)
        books = book_loader.get_books(params)

        return books

    @cli.command()
    def consumer():
        MessageBus.declare_scheme()
        # click.echo('echo working')
        MessageBus.consumer.run()

    return cli
