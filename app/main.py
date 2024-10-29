import typer
from . import utils

app = typer.Typer()


@app.command()
def initiate():
    try:
        utils.initiate_app()
    except FileNotFoundError as e:
        error_message = typer.style(
            str(e),
            fg=typer.colors.RED
        )
        typer.echo(error_message)
        raise typer.Exit(1)


@app.command()
def backup_dj_app(app_title: str):
    pass
