import os
import pickle
import google.auth.transport.requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from app import settings


class Gdrive:
    def __init__(self):
        self.client = self.__get_client()
        
    def __get_client(self):
        creds = None
        token_file = settings.TOKEN_FILE
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(settings.SECRETS_FILE, settings.GDRIVE_SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        return build('drive', 'v3', credentials=creds)


    def upload_file(self, file_path, parent_id) -> str:
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [parent_id]
        }
        media = MediaFileUpload(file_path)
        file = self.client.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return file.get('id')


    def create_folder(self, folder_name, parent_id=None) -> str:
        folder_metadata = {
            'mimeType': 'application/vnd.google-apps.folder',
            'name': folder_name
        }
        if parent_id:
            folder_metadata['parents'] = [parent_id]
        folder = self.client.files().create(body=folder_metadata, fields='id').execute()
        return folder.get('id')
    
gdrive_client = Gdrive()
