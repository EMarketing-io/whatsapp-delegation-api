import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import requests
import io

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "/secrets/credentials.json")
SCOPES = ["https://www.googleapis.com/auth/drive"]
SHARED_DRIVE_ID = os.getenv("SHARED_DRIVE_ID")


def upload_to_drive(file_url):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    drive_service = build("drive", "v3", credentials=credentials)

    response = requests.get(file_url)
    response.raise_for_status()

    file_data = io.BytesIO(response.content)
    file_metadata = {
        "name": "whatsapp_audio.mp3",
        "parents": [SHARED_DRIVE_ID],
        "driveId": SHARED_DRIVE_ID,
    }

    media = MediaIoBaseUpload(file_data, mimetype="audio/mpeg", resumable=True)

    uploaded = (
        drive_service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )

    return uploaded["webViewLink"]
