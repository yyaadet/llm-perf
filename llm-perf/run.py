import click
from kimi import Kimi


@click.group
def cli():
    pass


@click.command()
@click.option("--cookie", required=True, type=str)
@click.option("--token", required=True, type=str)
@click.option("--chat_id", required=True, type=str)
def kimi(cookie, token, chat_id):
    llm = Kimi(False, cookie, token, chat_id)
    llm.test_with_requests()
cli.add_command(kimi)


if __name__ == '__main__':
    cli()
