import json

from django.test import SimpleTestCase

from pipeline import llm
from pipeline.stages import BUILDING, DONE, FAILED, QUEUED, READING, TESTING, can_move


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