import json
from unittest.mock import patch

from django.test import SimpleTestCase

from pipeline import llm
from pipeline.orchestrator import MAX_ATTEMPTS, run_pipeline
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
    def test_lesson_becomes_a_finished_game(self):
        run = run_pipeline("Water freezes into ice and boils into steam.")
        self.assertEqual(run["step"], DONE)
        self.assertEqual(len(run["questions"]), 2)
        self.assertEqual(
            run["history"],
            [QUEUED, READING, WRITING_QUESTIONS, CHECKING, BUILDING, TESTING, DONE],
        )

    def test_empty_lesson_fails_right_away(self):
        run = run_pipeline("   ")
        self.assertEqual(run["step"], FAILED)
        self.assertEqual(run["error"], "The lesson is empty.")

    def test_game_that_keeps_breaking_fails_after_3_tries(self):
        # Pretend the play-test always finds a problem.
        with patch("pipeline.orchestrator.play_test", return_value=(False, ["Button does nothing"])):
            run = run_pipeline("Water freezes into ice.")
        self.assertEqual(run["step"], FAILED)
        self.assertEqual(run["attempts"], MAX_ATTEMPTS)
        self.assertIsNone(run["game_html"])