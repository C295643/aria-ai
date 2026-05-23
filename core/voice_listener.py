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
        _model = WhisperModel(model_size, device="cuda", compute_type="float16")
        print("[ARIA] Model ready.")
    return _model


def record_audio(duration_seconds: int = 5) -> np.ndarray:
    print(f"[ARIA] Recording for {duration_seconds} seconds... Speak now.")
    audio = sd.rec(
        int(duration_seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
    )
    sd.wait()
    print("[ARIA] Recording complete.")
    return audio.flatten()


def transcribe(audio: np.ndarray, model_size: str = "base") -> str:
    model = _get_model(model_size)
    segments, _ = model.transcribe(audio, beam_size=5)
    return " ".join(segment.text.strip() for segment in segments)
