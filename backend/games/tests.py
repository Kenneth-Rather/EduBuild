"""Tests for the prototype game-generation endpoint."""

import json

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile


class GenerateGameTests(TestCase):
    """Verify the backend receives text and returns trivia JSON."""

    def test_generate_game_from_json(self):
        """Check that JSON lesson text produces two successful questions."""
        response = self.client.post(
            "/api/generate-game/",
            data=json.dumps({"text": "Cats are mammals."}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(len(response.json()["questions"]), 2)

    def test_generate_game_from_text_file(self):
        """Check that a UTF-8 .txt upload is accepted."""
        response = self.client.post(
            "/api/generate-game/",
            data={
                "lesson": SimpleUploadedFile(
                    "lesson.txt",
                    b"The water cycle.",
                    content_type="text/plain",
                )
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_empty_text_is_rejected(self):
        """Check that blank lesson text receives a useful client error."""
        response = self.client.post(
            "/api/generate-game/",
            data=json.dumps({"text": " "}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
