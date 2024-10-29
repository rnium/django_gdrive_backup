import os
from app.settings import BASE_DIR
from app.drive_utils import authenticate

def initiate_app():
    if not os.path.exists(BASE_DIR / 'client_secret.json'):
        raise FileNotFoundError('Client Secret not found')
    authenticate()
    print('initiated')