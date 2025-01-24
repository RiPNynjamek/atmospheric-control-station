from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import os

class Drive:
    def authenticate(self):
        # Check if service account credentials file exists
        if os.path.exists('credential-service.json'):
            creds = Credentials.from_service_account_file(
                'credential-service.json',
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
        else:
            raise Exception("Service account credentials file not found.")

        # Return the Drive API service instance
        return build('drive', 'v3', credentials=creds)
    
    def upload(self, service, file_path, mimetype, remoteFile=None):
        file_metadata = {
            'name': remoteFile if remoteFile else file_path.split('/')[-1],
            'parents': ['1D3Z1vI_YIPw5BSb_51wpI5Sk5msk0xs6']
            }
        media = MediaFileUpload(file_path, mimetype=mimetype)
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = uploaded_file.get('id')
        print(f'File uploaded: {file_id}')