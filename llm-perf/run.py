import click
from kimi import Kimi
from glm4 import GLM4
from chatgpt import ChatGPT


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


@click.command()
@click.option("--cookie", required=True, type=str)
@click.option("--token", required=True, type=str)
@click.option("--assistant_id", required=True, type=str)
@click.option("--conversion_id", required=False, type=str, default="")
def glm4(cookie, token, assistant_id, conversion_id):
    llm = GLM4(False, cookie, token, assistant_id, conversion_id)
    llm.test_with_requests()
cli.add_command(glm4)



@click.command()
def chatgpt35():
    llm = ChatGPT(False, None, None)
    llm.test_with_requests()
cli.add_command(chatgpt35)


if __name__ == '__main__':
    cli()
