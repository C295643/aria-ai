from core.voice_listener import record_audio, transcribe
from modules.note_taker import save_note

RECORD_SECONDS = 5
WHISPER_MODEL = "base"  # options: tiny, base, small, medium, large-v3


def main():
    print("=== ARIA — Voice to Note ===")
    print(f"Using Whisper model: {WHISPER_MODEL}")
    print("Press Ctrl+C to quit.\n")

    while True:
        input("Press Enter to start recording...")
        audio = record_audio(duration_seconds=RECORD_SECONDS)
        text = transcribe(audio, model_size=WHISPER_MODEL)

        word_count = len(text.strip().split())
        if word_count >= 3:
            print(f"[ARIA] Transcribed: {text}")
            save_note(text)
        elif text.strip():
            print(f"[ARIA] Ignored (too short): '{text.strip()}'")
        else:
            print("[ARIA] Nothing detected, note not saved.")


if __name__ == "__main__":
    main()
