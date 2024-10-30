import typer
import json
import os
import subprocess
from app import settings
from app.drive_utils import gdrive_client


class Config:
    def __init__(self):
        if os.path.exists(settings.CONFIG_FILE):
            with open(settings.CONFIG_FILE) as file:
                data = json.loads(file.read())
        else:
            data = {}
        self.root_folder_id = data.get('root_folder')
        self.projects = data.get('projects', {})

    @property
    def initialized(self):
        return bool(self.root_folder_id)

    def dump_config(self):
        config_data = {
            'root_folder': self.root_folder_id,
            'projects': self.projects
        }
        with open(settings.CONFIG_FILE, 'w') as file:
            json.dump(config_data, file, indent=4)

    def initialize_config_file(self):
        if os.path.exists(settings.CONFIG_FILE):
            raise FileExistsError('Config File Already Exists')
        root_folder_id = gdrive_client.create_folder('Django App Backup')
        self.root_folder_id = root_folder_id
        self.dump_config()

    def add_django_app(self, django_app_path, python_path, media_path):
        if not self.initialized:
            raise AttributeError('Client not initialized yet')
        django_app_path, python_path, media_path = tuple(
            map(os.path.normpath, [django_app_path, python_path, media_path])
        )
        app_name = os.path.basename(django_app_path)
        if app_name in self.projects:
            raise AttributeError('App already configured')
        app_folder_id = gdrive_client.create_folder(
            app_name, self.root_folder_id)
        self.projects[app_name] = {
            'app_path': django_app_path,
            'python_path': python_path,
            'media_path': media_path,
            'gdrive_folder': app_folder_id,
        }
        self.dump_config()

    def get_app_config(self, app_name):
        if not app_name in self.projects:
            raise AttributeError('App not configured')
        return self.projects[app_name]


CONFIG = Config()


def raise_for_typer_error(msg: str):
    error_message = typer.style(
        msg,
        fg=typer.colors.RED
    )
    typer.echo(error_message)
    raise typer.Exit(1)


def show_success(msg: str):
    error_message = typer.style(
        msg,
        fg=typer.colors.BRIGHT_GREEN
    )
    typer.echo(error_message)


def create_data_backup(app_name):
    config = CONFIG.get_app_config(app_name)
    with open(settings.BASE_DIR / 'backup.json', 'w') as file:
        subprocess.run(
            [
                config['python_path'],
                f"{config['app_path']}/manage.py",
                'dumpdata',
                '--natural-foreign',
                '--natural-primary',
                '-e', 'contenttypes',
                '-e', 'auth.Permission',
                '--indent', '2'
            ],
            check=True,
            stdout=file
        )
