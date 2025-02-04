import typer
import logging

from commands import etl

logger = logging.getLogger(__name__)

app = typer.Typer(
    add_completion  = False,   # disable completion hint
    no_args_is_help = False   # need to always execute main callback
)

app.add_typer(etl.app, name='etl')

INPUT_PATH = 'data/in/lotteria.html'
DB_NAME = 'testing'


@app.command()
def main():
    pass

if __name__ == "__main__":
    app()