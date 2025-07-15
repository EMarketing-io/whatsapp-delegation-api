from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from extract_tasks import extract_tasks
from parse_output import parse_structured_output
from write_output import write_to_sheet
from transcribe_audio import transcribe_audio
from google_drive_uploader import upload_to_drive

app = FastAPI()


def process_text_task(text):
    try:
        structured_output = extract_tasks(text)
        rows = parse_structured_output(structured_output, "text", text)
        write_to_sheet(rows)
    except Exception as e:
        print("❌ Text task processing failed:", str(e))


def process_audio_task(media_url):
    try:
        gdrive_url = upload_to_drive(media_url)
        transcription, source_link = transcribe_audio(gdrive_url)
        structured_output = extract_tasks(transcription)
        rows = parse_structured_output(structured_output, "audio", source_link)
        write_to_sheet(rows)
    except Exception as e:
        print("❌ Audio task processing failed:", str(e))


class ProcessRequest(BaseModel):
    choice: str
    gdrive_url: str | None = None
    text_input: str | None = None


@app.post("/process")
def process(req: ProcessRequest):
    try:
        print("🚀 Starting /process request")

        choice = req.choice.strip().lower()
        gdrive_url = req.gdrive_url.strip() if req.gdrive_url else ""
        text_input = req.text_input.strip() if req.text_input else ""
        source_link = ""

        print("📦 Choice received:", choice)

        if choice == "audio":
            if not gdrive_url:
                raise HTTPException(
                    status_code=400, detail="Missing Google Drive URL for audio choice."
                )
            print("🎧 Starting transcription for audio")
            transcription, source_link = transcribe_audio(gdrive_url)

        elif choice == "text":
            transcription = text_input
            source_link = text_input
            print("📝 Using text input directly")

        else:
            raise HTTPException(
                status_code=400, detail="Invalid choice. Use 'audio' or 'text'."
            )

        print("🧠 Extracting tasks")
        structured_output = extract_tasks(transcription)

        print("📋 Parsing structured output")
        rows = parse_structured_output(structured_output, choice, source_link)

        print(f"📤 Writing {len(rows)} rows to Google Sheet")
        write_to_sheet(rows)

        return {"message": f"{len(rows)} structured tasks added."}

    except Exception as e:
        print("❌ Full error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook")
async def receive_whatsapp(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        message = data.get("message", {})
        media_url = message.get("url")
        message_text = message.get("text", "")
        sender = data.get("user", {}).get("phone", "")

        if message.get("type") == "text" and message_text:
            if message_text.lower().startswith(("/task", "task")):
                command_text = message_text.split(" ", 1)[-1].strip()
                background_tasks.add_task(process_text_task, command_text)
                return {"status": "✅ Text task received", "from": sender}

        if message.get("type") in ["ptt", "document"] and message.get(
            "mime", ""
        ).startswith("audio/"):
            if media_url:
                background_tasks.add_task(process_audio_task, media_url)
                return {"status": "✅ Audio received", "from": sender}

        return {"status": "ignored", "reason": "No task trigger", "from": sender}
    except Exception as e:
        print("❌ Webhook error:", str(e))
        return {"error": str(e)}
