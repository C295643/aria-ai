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

ARIA is not listening while it waits for Enter. **Ctrl+C** stops ARIA, releases an active microphone recording, and prints `[ARIA] Stopped.` without a traceback. Restart ARIA after changing its code or microphone setting.

### Choose Your Microphone

ARIA uses the system default microphone unless `ARIA_INPUT_DEVICE` is set. Headphones used for playback do not necessarily supply the default microphone; Windows may still select a webcam or laptop input.

Stop ARIA first. List available devices:

```powershell
.\.venv\Scripts\python.exe -m sounddevice
```

Choose a device with input channels. In the **same PowerShell terminal**, set its name and host API, then start ARIA. This Sony headset is an example; replace it with a device from your list:

```powershell
$env:ARIA_INPUT_DEVICE = 'Headset (WH-1000XM4), MME'
.\.venv\Scripts\python.exe aria.py
```

After pressing Enter, confirm the selection before speaking:

```text
[ARIA] Microphone: Headset (WH-1000XM4), MME
[ARIA] Recording for 5 seconds... Speak now.
```

The override applies to this terminal session, not every VS Code terminal or future session. If the output says `[ARIA] Microphone: system default`, the override is not set in the process running ARIA. A microphone icon only indicates that an input is open, not that the intended microphone is receiving sound.

To return to the Windows default input, stop ARIA, run the following, and restart it:

```powershell
Remove-Item Env:ARIA_INPUT_DEVICE -ErrorAction SilentlyContinue
.\.venv\Scripts\python.exe aria.py
```

### Troubleshooting Audio

- **Nothing detected:** confirm the displayed microphone, check mute and input level in Windows Settings > System > Sound > Input, and speak during the five-second recording window.
- **Ignored (too short):** ARIA only routes transcriptions containing at least three words. Try "Take a note: buy groceries tomorrow."
- **First-run model download fails:** the Whisper `base` model must be downloaded from Hugging Face before it can run locally. Initial dependency and model downloads require internet access; inference runs on your machine once the models are available.
- **Where is the text saved?** Transcriptions are displayed in the terminal. Only commands classified as `save_note` create files in `notes/`; the `logs/` directory is not currently used.

## Tests

Run the microphone-selection and clean-shutdown regression tests without opening a microphone:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

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
