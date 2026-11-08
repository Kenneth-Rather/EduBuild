from django.contrib.auth.models import User
from django.test import TestCase

from .models import (
    Game,
    GameVersion,
    GenerationRequest,
    GenerationRun,
    Lesson,
    Question,
    ShareLink,
)


class GameDatabaseTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="test-password",
        )
        self.lesson = Lesson.objects.create(
            owner=self.teacher,
            title="The water cycle",
            source_text="Water evaporates, condenses, and precipitates.",
        )
        self.game = Game.objects.create(
            owner=self.teacher,
            lesson=self.lesson,
            title="Water cycle trivia",
            grade_level="4",
        )

    def test_generation_and_game_content_relationships(self):
        request = GenerationRequest.objects.create(
            requested_by=self.teacher,
            lesson=self.lesson,
            game=self.game,
            settings={"question_count": 5},
        )
        run = GenerationRun.objects.create(request=request, stage="write_questions")
        version = GameVersion.objects.create(
            game=self.game,
            version_number=1,
            created_by=self.teacher,
            config={"template": "trivia"},
        )
        question = Question.objects.create(
            version=version,
            order=1,
            prompt="What happens when water vapor cools?",
            answer_options=["It condenses", "It disappears"],
            correct_answer="It condenses",
            source_excerpt="Water vapor condenses when it cools.",
        )

        self.assertEqual(request.runs.get(), run)
        self.assertEqual(self.game.versions.get(), version)
        self.assertEqual(version.questions.get(), question)

    def test_share_link_has_unique_public_token(self):
        link = ShareLink.objects.create(game=self.game)

        self.assertIsNotNone(link.token)
        self.assertTrue(link.is_active)
        self.assertEqual(self.game.share_links.get(), link)
