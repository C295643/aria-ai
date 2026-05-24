# ARIA — Autonomous Robotic Intelligence Assistant
### Project Specification Document
**Version:** 0.2.0 — Phase 1 Complete  
**Status:** Active  
**Last Updated:** 2026-05-24  

---

## 1. Project Overview

**ARIA** is a fully local AI assistant designed to run entirely on the user's machine — no cloud APIs, no internet dependency. It listens for voice commands, processes them using local AI models, and executes tasks autonomously. The first capability milestone is voice-to-text note-taking.

The project is built incrementally: each phase adds a new capability layer on top of a stable foundation.

---

## 2. Core Philosophy

| Principle | Description |
|---|---|
| **100% Local** | All AI inference runs on-device. No data leaves the machine. |
| **Modular** | Each capability is a self-contained module that can be added or removed. |
| **Incremental** | Build one working layer at a time before adding complexity. |
| **Open** | Built with open-source tools only. |
| **Documented** | This spec evolves alongside the project. |

---

## 3. Tech Stack

### 3.1 Local LLM Engine
- **Ollama** — runs and manages local language models
  - Recommended starter model: `llama3.2` (3B, fast, low RAM) or `mistral` (7B, smarter)
  - Provides an OpenAI-compatible local API at `http://localhost:11434`

### 3.2 Voice Input (Speech-to-Text)
- **faster-whisper** (`large-v3` model recommended for this machine)
  - Runs fully on-device via CUDA (RTX 4060)
  - No microphone data sent to cloud
  - Significantly faster than original `openai-whisper`

### 3.3 Agent Framework
- **Python** — primary language
- **LangChain** or direct Ollama API calls — orchestration layer

### 3.4 Text-to-Speech (optional, future)
- **Piper TTS** or **Coqui TTS** — local voice responses

### 3.5 Development Environment
- **VSCode** — IDE
- **GitHub** — version control and project tracking
- **Python 3.11+** — runtime
- **venv** — virtual environment management
- **Windows 11** — host OS
- **CUDA 13.0** — GPU acceleration for Whisper and future inference (Driver 581.32, confirmed)

---

## 4. Repository Structure (Planned)

```
aria/
├── README.md
├── PROJECT_SPEC.md          ← this file
├── requirements.txt
├── .env.example
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── agent.py             ← main agent loop
│   ├── voice_listener.py    ← microphone capture + STT
│   └── llm_client.py        ← Ollama interface
│
├── modules/
│   ├── __init__.py
│   ├── note_taker.py        ← Phase 1: save voice → .txt notes
│   └── (future modules)
│
├── notes/                   ← output folder for saved notes
├── logs/
└── tests/
```

---

## 5. Development Phases

### ✅ Phase 0 — Foundation (Complete)

**Goal:** Get the environment set up and document the plan.

- [x] Create GitHub repository
- [x] Set up VSCode workspace
- [x] Install Ollama and pull a starter model (`mistral`)
- [x] Create Python virtual environment
- [x] Test basic LLM response from Ollama API
- [x] Commit `PROJECT_SPEC_1.md` and `README.md`

---

### ✅ Phase 1 — Voice-to-Note (Complete)

**Goal:** Say a command → ARIA saves it as a `.txt` file.

**How it works:**
1. User speaks into microphone
2. Whisper converts speech to text (locally, CPU mode)
3. Output saved as a timestamped `.txt` file in `/notes`

**Deliverables:**
- [x] `voice_listener.py` — captures audio and runs Whisper STT
- [x] `note_taker.py` — writes the transcription to disk
- [x] Basic CLI runner (`python aria.py`)
- [x] Notes saved as: `notes/YYYY-MM-DD_HH-MM-SS.txt`

**Acceptance Criteria:**

- [x] Say a sentence → file appears in `/notes` with correct text within ~5 seconds

**Implementation Notes:**

- Whisper running in CPU mode (`int8`) — CUDA DLL path issue on Windows to revisit
- 3-word minimum filter added to suppress Whisper hallucinations on short/silent audio

---

### 🔲 Phase 2 — Command Understanding
**Goal:** ARIA understands *what you want*, not just what you said.

**How it works:**
1. Transcribed text is sent to local LLM
2. LLM identifies intent (e.g., "take a note", "remind me", "search for...")
3. ARIA routes to the appropriate module

**Deliverables:**
- [ ] Intent classifier prompt
- [ ] Command router in `agent.py`
- [ ] At least 2 routable commands

---

### 🔲 Phase 3 — Wake Word Detection
**Goal:** ARIA listens passively and activates only on a trigger word (e.g., "Hey ARIA").

**Tools:** `pvporcupine` (local wake word, free tier) or `openWakeWord`

**Deliverables:**
- [ ] Always-on listener with low CPU usage
- [ ] Wake word activates STT → agent loop

---

### 🔲 Phase 4 — Memory & Context
**Goal:** ARIA remembers things across sessions.

**How it works:**
- Short-term: conversation history in context window
- Long-term: vector store (Chroma or FAISS) for note retrieval

**Deliverables:**
- [ ] Notes are indexed into a vector DB
- [ ] ARIA can answer: "What did I note about X?"

---

### 🔲 Phase 5 — Expanded Capabilities (TBD)
Ideas for future modules — to be prioritized based on needs:

| Module | Description |
|---|---|
| Reminders | Set and trigger time-based reminders locally |
| File Search | Search local files by voice query |
| Voice Response | ARIA speaks back using local TTS |
| Code Assistant | Ask coding questions, get answers read aloud |
| Home Automation | Control local devices via voice (MQTT, HA) |
| Browser Control | Open URLs, search the web by voice |

---

## 6. Hardware Requirements

| Tier | RAM | CPU | GPU | Notes |
|---|---|---|---|---|
| Minimum | 8 GB | Modern quad-core | None | CPU-only inference, slower |
| Recommended | 16 GB | 8+ core | 6 GB VRAM | Faster STT + LLM |
| Ideal | 32 GB | 12+ core | 12+ GB VRAM | Smooth 7B models |

### 6.1 This Machine — Dell XPS 16 (XPS16JV)

| Component | Spec | Notes |
|---|---|---|
| CPU | Intel Core Ultra 9 185H (16-core, 2.5 GHz) | Excellent for CPU fallback tasks |
| RAM | 32 GB | Comfortably fits 7B models fully in RAM |
| GPU | NVIDIA RTX 4060 Laptop (8188 MB VRAM) | CUDA 13.0 confirmed, driver 581.32 |
| GPU (secondary) | Intel Arc (128 MB) | Not usable for inference — ignore |
| Storage | ~167 GB free | Sufficient; models are 4–8 GB each |
| OS | Windows 11, 64-bit | |

**Tier: Recommended → approaching Ideal**

> This machine can run **7B parameter models** (like `mistral:7b` or `llama3.1:8b`) fully on the GPU with fast inference. Whisper `large-v3` is also viable for highest STT accuracy. No compromises needed on model size.

### 6.2 Recommended Models for This Machine

| Use Case | Model | Size | Why |
|---|---|---|---|
| Main LLM (Phase 2+) | `mistral:7b` or `llama3.1:8b` | ~4.5 GB | Fast on RTX 4060, great instruction following |
| Lightweight LLM | `llama3.2:3b` | ~2 GB | Near-instant responses if speed is priority |
| Speech-to-Text | `faster-whisper large-v3` | ~3 GB | Best accuracy, runs well on this GPU |
| STT (lighter option) | `faster-whisper base` | ~150 MB | Fastest, good enough for clear speech |

---

## 7. Privacy & Security

- **No telemetry.** No data is sent outside the machine.
- **Microphone access** is only active during recording (or after wake word in Phase 3).
- **No API keys required** for core functionality.
- `.env` file used for any optional integrations — never committed to Git.

---

## 8. Getting Started (Quickstart — to be expanded)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/aria.git
cd aria

# 2. Create virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Ollama and pull a model
# Download from https://ollama.com
ollama pull mistral

# 5. Run ARIA
python aria.py
```

---

## 9. Open Questions & Decisions Log

| # | Question | Decision | Date |
|---|---|---|---|
| 1 | Which STT engine? | `faster-whisper` (best speed/accuracy balance) | 2026-05-24 |
| 2 | Which Whisper model for Phase 1? | `base` — good accuracy, fast on CPU | 2026-05-24 |
| 3 | GPU or CPU for Whisper? | CPU (`int8`) for now — CUDA DLL issue on Windows to revisit | 2026-05-24 |
| 4 | Wake word engine? | Evaluate `openWakeWord` vs `porcupine` | Phase 3 |
| 5 | GUI or CLI only? | CLI first, GUI optional later | TBD |

---

## 10. Changelog

| Version | Date | Changes |
|---|---|---|
| 0.2.0 | 2026-05-24 | Phase 1 complete — Voice-to-Note working; CPU mode; 3-word filter added |
| 0.1.2 | 2026-05-23 | Confirmed CUDA 13.0, driver 581.32, 8188 MB VRAM available |
| 0.1.1 | 2026-05-22 | Added hardware profile (Dell XPS 16), updated model recommendations and Windows quickstart |
| 0.1.0 | 2026-05-22 | Initial blueprint created |

---

*This document is a living specification. Update it as goals evolve.*