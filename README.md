# ARIA — Autonomous Robotic Intelligence Assistant

A fully local AI assistant that runs entirely on your machine — no cloud APIs, no internet dependency, no data leaving your device.

## Current Capabilities

- **Voice commands** — ARIA transcribes speech and uses a local Ollama model to classify it as a request to save a note, list recent notes, or an unknown command
- **Note management** — save transcriptions as timestamped `.txt` files or list the five most recent notes

## Tech Stack

| Component | Tool |
| --- | --- |
| Speech-to-Text | `faster-whisper` (Whisper `base` model, CPU) |
| LLM Engine | Ollama (`mistral`, local intent classification) |
| Language | Python 3.11+ |
| Platform | Windows 11, VSCode |

## Getting Started

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running, with the `mistral` model available

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

# 4. Download the configured local language model
ollama pull mistral
```

### Run

```powershell
.venv\Scripts\activate
python aria.py
```

Press **Enter** to start a 5-second recording. Say a command to save a note or list your recent notes; ARIA transcribes it and asks the local model to classify the intent. Saved notes appear in `notes/YYYY-MM-DD_HH-MM-SS.txt`. Press **Ctrl+C** to quit.

## Project Structure

```text
aria-ai/
├── aria.py                  ← CLI entry point
├── core/
│   ├── voice_listener.py    ← microphone capture + Whisper STT
│   ├── agent.py             ← intent classification and command routing
│   └── llm_client.py        ← local Ollama interface
├── modules/
│   └── note_taker.py        ← saves and lists notes in /notes
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
| 2 — Command Understanding | 🔄 In progress | Local LLM routes save-note and list-notes commands |
| 3 — Wake Word | 🔲 Planned | Always-on listener, activates on trigger word |
| 4 — Memory & Context | 🔲 Planned | Vector DB for note retrieval across sessions |
| 5 — Expanded Capabilities | 🔲 Future | Reminders, TTS, file search, browser control |

See [PROJECT_SPEC_1.md](PROJECT_SPEC_1.md) for the full specification.

## Privacy

All processing is 100% local. No microphone data, transcriptions, or notes are ever sent outside your machine.
