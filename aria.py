from core.voice_listener import record_audio, transcribe
from core.agent import handle

RECORD_SECONDS = 5
WHISPER_MODEL = "base"  # options: tiny, base, small, medium, large-v3


def main():
    print("=== ARIA — Voice Assistant ===")
    print(f"Using Whisper model: {WHISPER_MODEL}")
    print("Press Ctrl+C to quit.\n")

    while True:
        input("Press Enter to start recording...")
        audio = record_audio(duration_seconds=RECORD_SECONDS)
        text = transcribe(audio, model_size=WHISPER_MODEL)

        if text.strip():
            handle(text)
        else:
            print("[ARIA] Nothing detected.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[ARIA] Stopped.")
