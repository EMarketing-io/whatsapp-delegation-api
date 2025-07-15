from transcribe_audio import transcribe_audio
from transcribe_text import transcribe_text
from extract_tasks import extract_tasks
from parse_output import parse_structured_output
from write_output import write_to_sheet


def main():
    choice = input("Enter 'audio' or 'text': ").strip().lower()
    source_link = ""
    transcription = ""

    if choice == "audio":
        gdrive_url = input("Enter Google Drive share link to your audio file: ").strip()
        transcription, source_link = transcribe_audio(gdrive_url)
    elif choice == "text":
        transcription = transcribe_text()
        source_link = transcription

    else:
        raise ValueError("Invalid input. Use 'audio' or 'text'.")

    structured_output = extract_tasks(transcription)
    rows = parse_structured_output(structured_output, choice, source_link)
    write_to_sheet(rows)
    print(f"✅ {len(rows)} structured tasks added to your Google Sheet.")


if __name__ == "__main__":
    main()
