from urllib.error import URLError

from core.llm_client import DEFAULT_MODEL, ask
from modules.note_taker import save_note, list_notes

INTENT_PROMPT = """You are a voice assistant intent classifier. The user said the following:

"{text}"

Classify their intent as exactly one of these labels:
- save_note: the user wants to save, record, note, or remember something
- list_notes: the user wants to see, list, read, or recall their notes
- unknown: the intent is unclear or doesn't match any of the above

Reply with ONLY the label, nothing else."""


def classify_intent(text: str) -> str:
    response = ask(INTENT_PROMPT.format(text=text))
    response = response.lower().strip().strip(".")
    if response in ("save_note", "list_notes"):
        return response
    return "unknown"


def handle(text: str) -> None:
    print(f"[ARIA] You said: {text}")
    try:
        intent = classify_intent(text)
    except (URLError, TimeoutError, ConnectionError):
        print(
            "[ARIA] Could not reach Ollama or complete the request. "
            "Check that Ollama is running and try again. "
            f"If the model is missing, run: ollama pull {DEFAULT_MODEL}"
        )
        return
    print(f"[ARIA] Intent: {intent}")

    if intent == "save_note":
        save_note(text)
    elif intent == "list_notes":
        notes = list_notes()
        if notes:
            print("\n[ARIA] Your recent notes:")
            for entry in notes:
                print(f"  {entry}")
        else:
            print("[ARIA] No notes found.")
    else:
        print("[ARIA] I didn't understand that. Please try again.")
