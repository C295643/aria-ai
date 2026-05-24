# ARIA — Autonomous Robotic Intelligence Assistant

A fully local AI assistant that runs entirely on your machine — no cloud APIs, no internet dependency, no data leaving your device.

## Current Capabilities

- **Voice-to-Note** — speak a sentence, ARIA transcribes it and saves it as a timestamped `.txt` file in `/notes`

## Tech Stack

| Component | Tool |
| --- | --- |
| Speech-to-Text | `faster-whisper` (Whisper `base` model, CPU) |
| LLM Engine | Ollama (used from Phase 2 onward) |
| Language | Python 3.11+ |
| Platform | Windows 11, VSCode |

## Getting Started

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed (required from Phase 2 onward)

### Setup

```powershell
# 1. Clone the repo
git clone git@github.com:C295643/aria-ai.git
cd aria-ai

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run

```powershell
.venv\Scripts\activate
python aria.py
```

Press **Enter** to start a 5-second recording. ARIA will transcribe your speech and save it to `notes/YYYY-MM-DD_HH-MM-SS.txt`. Press **Ctrl+C** to quit.

## Project Structure

```text
aria-ai/
├── aria.py                  ← CLI entry point
├── core/
│   ├── voice_listener.py    ← microphone capture + Whisper STT
│   └── llm_client.py        ← Ollama interface (Phase 2+)
├── modules/
│   └── note_taker.py        ← saves transcriptions to /notes
├── notes/                   ← output folder (gitignored)
├── logs/                    ← log output (gitignored)
├── requirements.txt
└── PROJECT_SPEC_1.md        ← living specification document
```

## Development Phases

| Phase | Status | Description |
| --- | --- | --- |
| 0 — Foundation | ✅ Complete | Environment setup, repo, Ollama, Python venv |
| 1 — Voice-to-Note | ✅ Complete | Voice recording → Whisper STT → `.txt` note |
| 2 — Command Understanding | 🔲 Next | LLM identifies intent and routes to the right module |
| 3 — Wake Word | 🔲 Planned | Always-on listener, activates on trigger word |
| 4 — Memory & Context | 🔲 Planned | Vector DB for note retrieval across sessions |
| 5 — Expanded Capabilities | 🔲 Future | Reminders, TTS, file search, browser control |

See [PROJECT_SPEC_1.md](PROJECT_SPEC_1.md) for the full specification.

## Privacy

All processing is 100% local. No microphone data, transcriptions, or notes are ever sent outside your machine.
