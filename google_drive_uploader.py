import os
import tempfile
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from config import SERVICE_ACCOUNT_FILE, FOLDER_ID


def upload_to_drive(media_url):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"]
    )
    drive_service = build("drive", "v3", credentials=creds)

    response = requests.get(media_url)
    if response.status_code != 200:
        raise Exception("Failed to download audio from WhatsApp")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:
        audio_file.write(response.content)
        audio_path = audio_file.name

    file_metadata = {"name": os.path.basename(audio_path), "parents": [FOLDER_ID]}
    media = MediaFileUpload(audio_path, mimetype="audio/mpeg")
    uploaded = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    os.remove(audio_path)

    return f"https://drive.google.com/file/d/{uploaded['id']}/view"
