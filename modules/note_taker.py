from datetime import datetime
from pathlib import Path

NOTES_DIR = Path(__file__).parent.parent / "notes"


def save_note(text: str) -> Path:
    NOTES_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    note_path = NOTES_DIR / f"{timestamp}.txt"
    note_path.write_text(text, encoding="utf-8")
    print(f"[ARIA] Note saved: {note_path}")
    return note_path
