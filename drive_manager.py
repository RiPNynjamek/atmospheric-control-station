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

        # Old version with token management
        # if os.path.exists('token.json'):
        #     creds = Credentials.from_authorized_user_file('token.json')

        #     if creds and creds.expired and creds.refresh_token:
        #         creds.refresh(Request())
        #         with open('token.json', 'w') as token:
        #             token.write(creds.to_json())

        #     # If no valid credentials are available (either expired and can't refresh or never obtained)
        #     if not creds or not creds.valid:
        #         if creds and creds.expired and creds.refresh_token:
        #             creds.refresh(Request())
        #         else:
        #             # Re-authenticate and get new refresh token
        #             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive.file'])
        #             creds = flow.run_local_server(port=0)
        #             # Save credentials for future use
        #             with open('token.json', 'w') as token:
        #                 token.write(creds.to_json())
        # else:
        #     SCOPES = ["https://wwww.googleapis.com/auth/drive.file"]
        #     flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        #     creds = flow.run_local_server(port=0)
        # return build('drive', 'v3', credentials=creds)
    
    def upload(self, service, file_path):
        file_metadata = {
            'name': file_path.split('/')[-1],
            'parents': ['1D3Z1vI_YIPw5BSb_51wpI5Sk5msk0xs6']
            }
        media = MediaFileUpload(file_path, mimetype='image/png')
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = uploaded_file.get('id')
        print(f'File uploaded: {file_id}')