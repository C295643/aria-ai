import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import aria
from core import agent


class CommandTests(unittest.TestCase):
    def test_nonempty_transcriptions_reach_router(self):
        for text in ("List notes", "Read notes", "Hello", "Take a note for tomorrow"):
            with (
                self.subTest(text=text),
                patch("builtins.input", side_effect=["", KeyboardInterrupt]),
                patch.object(aria, "record_audio"),
                patch.object(aria, "transcribe", return_value=text),
                patch.object(aria, "handle") as handle,
                redirect_stdout(io.StringIO()),
            ):
                with self.assertRaises(KeyboardInterrupt):
                    aria.main()
                handle.assert_called_once_with(text)

    def test_empty_transcriptions_do_not_reach_router(self):
        for text in ("", "   "):
            output = io.StringIO()
            with (
                self.subTest(text=text),
                patch("builtins.input", side_effect=["", KeyboardInterrupt]),
                patch.object(aria, "record_audio"),
                patch.object(aria, "transcribe", return_value=text),
                patch.object(aria, "handle") as handle,
                redirect_stdout(output),
            ):
                with self.assertRaises(KeyboardInterrupt):
                    aria.main()
                handle.assert_not_called()
                self.assertIn("[ARIA] Nothing detected.", output.getvalue())

    def test_ollama_transport_errors_are_retryable(self):
        errors = (
            URLError("Connection refused"),
            HTTPError("http://localhost:11434/api/generate", 503, "Unavailable", {}, None),
            TimeoutError("Request timed out"),
            ConnectionResetError("Connection reset"),
        )
        for error in errors:
            if isinstance(error, HTTPError):
                self.addCleanup(error.close)
            output = io.StringIO()
            with (
                self.subTest(error=type(error).__name__),
                patch.object(agent, "ask", side_effect=error),
                patch.object(agent, "save_note") as save_note,
                patch.object(agent, "list_notes") as list_notes,
                redirect_stdout(output),
            ):
                agent.handle("List notes")
            save_note.assert_not_called()
            list_notes.assert_not_called()
            self.assertIn("Check that Ollama is running and try again.", output.getvalue())

    def test_loop_accepts_next_command_after_ollama_failure(self):
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=["", "", KeyboardInterrupt]),
            patch.object(aria, "record_audio"),
            patch.object(aria, "transcribe", return_value="List notes"),
            patch.object(agent, "ask", side_effect=[URLError("Connection refused"), "list_notes"]),
            patch.object(agent, "list_notes", return_value=[]) as list_notes,
            redirect_stdout(output),
        ):
            with self.assertRaises(KeyboardInterrupt):
                aria.main()
        list_notes.assert_called_once_with()
        self.assertIn("Check that Ollama is running and try again.", output.getvalue())
        self.assertIn("[ARIA] No notes found.", output.getvalue())


if __name__ == "__main__":
    unittest.main()