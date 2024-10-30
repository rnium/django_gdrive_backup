from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / 'config.json'
SECRETS_FILE = BASE_DIR / 'client_secret.json'
TOKEN_FILE = BASE_DIR / 'token.pickle'

GDRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']