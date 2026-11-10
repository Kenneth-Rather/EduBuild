"""Tests for the prototype game-generation endpoint."""

import json

from unittest.mock import patch

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from pipeline import llm
from .models import GameRecord

# Tests never call the real AI, so they are free and always give the same result.
llm.USE_FAKE_AI = True


class GenerateGameTests(TestCase):
    """Verify the backend receives text and returns trivia JSON."""

    def test_generate_game_from_json(self):
        """Check that JSON lesson text produces two successful questions."""
        response = self.client.post(
            "/api/generate-game/",
            data={
                "text": "Cats are mammals.",
                "username": "Dylan",
                "name": "Science Trivia",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(len(response.json()["questions"]), 2)
        record = GameRecord.objects.get()
        self.assertEqual(record.username, "Dylan")
        self.assertEqual(record.game_name, "Science Trivia")

    def test_generate_game_from_text_file(self):
        """Check that a UTF-8 .txt upload is accepted."""
        response = self.client.post(
            "/api/generate-game/",
            data={
                "lesson": SimpleUploadedFile(
                    "lesson.txt",
                    b"The water cycle.",
                    content_type="text/plain",
                ),
                "username": "Mia",
                "name": "Water Cycle Quiz",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        record = GameRecord.objects.get()
        self.assertEqual(record.username, "Mia")
        self.assertEqual(record.game_name, "Water Cycle Quiz")

    def test_empty_text_is_rejected(self):
        """Check that blank lesson text receives a useful client error."""
        response = self.client.post(
            "/api/generate-game/",
            data=json.dumps({"text": " "}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_ai_failure_returns_error(self):
        """Check that a broken AI answer becomes a clear error, not a crash."""
        with patch("pipeline.orchestrator.llm.ask", return_value="not json"):
            response = self.client.post(
                "/api/generate-game/",
                data=json.dumps({"text": "Cats are mammals."}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json()["status"], "error")