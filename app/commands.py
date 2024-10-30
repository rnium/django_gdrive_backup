import os
import typer
from app import settings, utils
from app.utils import CONFIG

app = typer.Typer()


@app.command()
def initiate():
    try:
        if not os.path.exists(settings.SECRETS_FILE):
            raise FileNotFoundError('Client Secret not found')
        CONFIG.initialize_config_file()
    except FileNotFoundError as e:
        utils.raise_for_typer_error(str(e))
    except Exception as e:
        utils.raise_for_typer_error(f"Error: {str(e)}")


@app.command()
def add_app(app_path, python_path, media_path):
    try:
        CONFIG.add_django_app(app_path, python_path, media_path)
    except Exception as e:
        utils.raise_for_typer_error(f"Error: {str(e)}")
    utils.show_success('App added')


@app.command()
def backup_app(app_name: str):
    try:
        utils.create_data_backup(app_name)
    except Exception as e:
        utils.raise_for_typer_error(str(e))
    utils.show_success('Backup Created')
