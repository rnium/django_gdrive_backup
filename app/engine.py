import os
from app.settings import BASE_DIR
from app import utils


def initiate_app():
    if not os.path.exists(BASE_DIR / 'client_secret.json'):
        raise FileNotFoundError('Client Secret found')
    utils.CONFIG.initialize_config_file()



    