import typer
import json
import os
import subprocess
import zipfile
from datetime import datetime
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
        
    def list_django_apps(self):
        for idx, app_title in enumerate(self.projects.keys()):
            print(f"{idx+1}. {app_title}")

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
        fg=typer.colors.GREEN
    )
    typer.echo(error_message)
    
def get_filenames():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    backup_file = settings.TEMP_DIR / f'backup_{timestamp}.json'
    zip_file_path = settings.TEMP_DIR / f'archive_{timestamp}.zip'
    return (backup_file, zip_file_path)

def create_zip(zip_name, media_path, db_backup_file_path):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, dirs, files in os.walk(media_path):
            for file in files:
                file_full_path = os.path.join(root, file)
                arcname = os.path.relpath(file_full_path, os.path.dirname(media_path))
                zipf.write(file_full_path, arcname)
        
        zipf.write(db_backup_file_path, os.path.basename(db_backup_file_path))
        
def cleanup_files(*file_paths):
    for fp in file_paths:
        if os.path.isfile(fp):
            os.remove(fp)

def perform_data_backup(app_name):
    config = CONFIG.get_app_config(app_name)
    os.makedirs(settings.TEMP_DIR, exist_ok=True)
    backup_file, zip_file_path = get_filenames()
    with open(backup_file, 'w') as file:
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
    create_zip(zip_file_path, config.get('media_path'), backup_file)
    gdrive_client.upload_file(zip_file_path, config.get('gdrive_folder'))
    cleanup_files(backup_file, zip_file_path)
