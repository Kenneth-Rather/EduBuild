from django.test import SimpleTestCase

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