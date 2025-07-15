import tempfile
import os
import requests
import openai
import subprocess
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def transcribe_audio(gdrive_url):
    # Extract file ID from Google Drive link
    file_id = gdrive_url.split("/d/")[1].split("/")[0] if "/d/" in gdrive_url else None
    if not file_id:
        raise ValueError("Invalid Google Drive link.")

    source_link = f"https://drive.google.com/file/d/{file_id}/view"
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)

    if "html" in response.headers.get("Content-Type", ""):
        raise Exception("Invalid or private Google Drive audio file.")

    suffix = ".oga"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_audio:
        tmp_audio.write(response.content)
        tmp_audio_path = tmp_audio.name

    converted_path = tmp_audio_path.replace(suffix, ".mp3")

    # 🔁 Convert using ffmpeg via subprocess
    try:
        print(f"🔁 Running ffmpeg on: {tmp_audio_path}")
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", tmp_audio_path, converted_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("✅ ffmpeg conversion successful")
    except subprocess.CalledProcessError as e:
        print("❌ ffmpeg failed with error:")
        print(e.stderr.decode())
        raise

    # 🧠 Transcribe using Whisper
    try:
        with open(converted_path, "rb") as audio_file:
            transcript_response = openai.Audio.translate("whisper-1", audio_file)
            print("📝 Transcription result:", transcript_response)
    except Exception as e:
        print("❌ Whisper failed:", e)
        raise
    finally:
        os.remove(tmp_audio_path)
        os.remove(converted_path)

    transcription_text = transcript_response.get("text", "").strip()
    if not transcription_text:
        raise Exception("Whisper returned empty transcription.")

    return transcription_text, source_link
