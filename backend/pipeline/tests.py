import json
from unittest.mock import patch

from django.test import SimpleTestCase

from pipeline import llm
from pipeline.orchestrator import run_pipeline
from pipeline.stages import (
    BUILDING,
    CHECKING,
    DONE,
    FAILED,
    QUEUED,
    READING,
    TESTING,
    WRITING_QUESTIONS,
    can_move,
)

LESSON = "When water gets very cold, it freezes into ice. When water gets very hot, it boils and turns into steam."


class StageTests(SimpleTestCase):
    def test_normal_next_step_is_allowed(self):
        self.assertTrue(can_move(QUEUED, READING))

    def test_skipping_steps_is_blocked(self):
        self.assertFalse(can_move(QUEUED, DONE))

    def test_failed_play_test_can_go_back_for_repair(self):
        self.assertTrue(can_move(TESTING, BUILDING))

    def test_failed_is_the_end(self):
        self.assertFalse(can_move(FAILED, READING))


class FakeAITests(SimpleTestCase):
    def test_writer_gives_back_questions(self):
        reply = llm.ask("writer", "any lesson text")
        data = json.loads(reply)
        self.assertEqual(len(data["questions"]), 2)

    def test_unknown_role_is_an_error(self):
        with self.assertRaises(ValueError):
            llm.ask("chef", "hello")


class OrchestratorTests(SimpleTestCase):
    def test_lesson_becomes_checked_questions(self):
        run = run_pipeline(LESSON)
        self.assertEqual(run["step"], DONE)
        self.assertEqual(len(run["questions"]), 2)
        self.assertEqual(run["history"], [QUEUED, READING, WRITING_QUESTIONS, CHECKING, DONE])

    def test_empty_lesson_fails_right_away(self):
        run = run_pipeline("   ")
        self.assertEqual(run["step"], FAILED)
        self.assertEqual(run["error"], "The lesson is empty.")

    def test_bad_ai_answer_fails(self):
        # Pretend the AI replied with plain text instead of JSON.
        with patch("pipeline.orchestrator.llm.ask", return_value="Sorry, I can't help with that."):
            run = run_pipeline(LESSON)
        self.assertEqual(run["step"], FAILED)
        self.assertEqual(run["questions"], [])

    def test_unsupported_question_is_removed(self):
        # Pretend the verifier says question 2 is NOT in the lesson.
        verdict = json.dumps({"results": [
            {"question_number": 1, "supported": True},
            {"question_number": 2, "supported": False},
        ]})
        real_ask = llm.ask

        def fake_ask(role, prompt):
            return verdict if role == "verifier" else real_ask(role, prompt)

        with patch("pipeline.orchestrator.llm.ask", side_effect=fake_ask):
            run = run_pipeline(LESSON)
        self.assertEqual(run["step"], DONE)
        self.assertEqual(len(run["questions"]), 1)