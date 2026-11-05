import io
from pathlib import Path
import runpy
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import numpy as np

from core import voice_listener


ENTRY_POINT = Path(__file__).resolve().parents[1] / "aria.py"


class ShutdownTests(unittest.TestCase):
    def test_recording_uses_selected_microphone_or_system_default(self):
        for selected in ("", "Headset (WH-1000XM4), MME"):
            output = io.StringIO()
            with (
                self.subTest(selected=selected),
                patch.dict(voice_listener.os.environ, {"ARIA_INPUT_DEVICE": selected}),
                patch.object(voice_listener.sd, "rec", return_value=np.zeros((160, 1))) as record,
                patch.object(voice_listener.sd, "wait"),
                patch.object(voice_listener.sd, "stop"),
                redirect_stdout(output),
            ):
                voice_listener.record_audio()
            self.assertEqual(record.call_args.kwargs["device"], selected or None)
            self.assertIn(f"[ARIA] Microphone: {selected or 'system default'}", output.getvalue())

    def test_ctrl_c_while_idle_exits_cleanly(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=KeyboardInterrupt), redirect_stdout(output):
            runpy.run_path(str(ENTRY_POINT), run_name="__main__")
        self.assertIn("[ARIA] Stopped.", output.getvalue())

    def test_ctrl_c_during_recording_stops_microphone_and_exits(self):
        output = io.StringIO()
        with (
            patch("builtins.input", return_value=""),
            patch.object(voice_listener.sd, "rec"),
            patch.object(voice_listener.sd, "wait", side_effect=KeyboardInterrupt),
            patch.object(voice_listener.sd, "stop") as stop,
            patch.object(voice_listener, "transcribe") as transcribe,
            redirect_stdout(output),
        ):
            runpy.run_path(str(ENTRY_POINT), run_name="__main__")
        stop.assert_called_once_with()
        transcribe.assert_not_called()
        self.assertIn("[ARIA] Stopped.", output.getvalue())
        self.assertNotIn("Recording complete.", output.getvalue())

    def test_completed_recording_still_returns_audio(self):
        audio = np.zeros((160, 1), dtype=np.float32)
        with (
            patch.object(voice_listener.sd, "rec", return_value=audio),
            patch.object(voice_listener.sd, "wait"),
            patch.object(voice_listener.sd, "stop") as stop,
            redirect_stdout(io.StringIO()),
        ):
            result = voice_listener.record_audio()
        stop.assert_called_once_with()
        np.testing.assert_array_equal(result, audio.flatten())


if __name__ == "__main__":
    unittest.main()