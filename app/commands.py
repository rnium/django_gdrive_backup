import typer
from . import engine
from . import utils

app = typer.Typer()


@app.command()
def initiate():
    try:
        engine.initiate_app()
    except FileNotFoundError as e:
        utils.raise_for_typer_error(str(e))
    except Exception as e:
        utils.raise_for_typer_error(f"Error: {str(e)}")


@app.command()
def backup_dj_app(app_title: str):
    conf = utils.Config()
    conf.initialize_config_file('foobarbaz')
