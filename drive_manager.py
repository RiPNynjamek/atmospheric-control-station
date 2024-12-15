from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

import os

class Drive:
    
    def authenticate():
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            # If no valid credentials are available (either expired and can't refresh or never obtained)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Re-authenticate and get new refresh token
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive.file'])
                    creds = flow.run_local_server(port=0)
                    # Save credentials for future use
                    with open('token.json', 'w') as token:
                        token.write(creds.to_json())
        else:
            SCOPES = ["https://wwww.googleapis.com/auth/drive.file"]
            flow = InstalledAppFlow.from_clients_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        return build('drive', 'v3', credentials=creds)
    
    def upload(service, file_path):
        file_metadata = {
            'name': file_path.split('/')[-1],
            'parents': ['1D3Z1vl_YIPw5BSb_51wpl5Sk5msk0xs6']
            }
        media = MediaFileUpload(file_path, mimetype='image/png')
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = uploaded_file.get('id')
        print(f'File uploaded: {file_id}')