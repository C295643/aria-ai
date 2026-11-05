import os

import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "float32"

_model = None


def _get_model(model_size="base"):
    global _model
    if _model is None:
        print(f"[ARIA] Loading Whisper model '{model_size}'...")
        _model = WhisperModel(model_size, device="cpu", compute_type="int8")
        print("[ARIA] Model ready.")
    return _model


def record_audio(duration_seconds: int = 5) -> np.ndarray:
    device = os.environ.get("ARIA_INPUT_DEVICE") or None
    print(f"[ARIA] Microphone: {device or 'system default'}")
    print(f"[ARIA] Recording for {duration_seconds} seconds... Speak now.")
    audio = sd.rec(
        int(duration_seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        device=device,
    )
    try:
        sd.wait()
    finally:
        sd.stop()
    print("[ARIA] Recording complete.")
    return audio.flatten()


def transcribe(audio: np.ndarray, model_size: str = "base") -> str:
    model = _get_model(model_size)
    segments, _ = model.transcribe(audio, beam_size=5)
    return " ".join(segment.text.strip() for segment in segments)
