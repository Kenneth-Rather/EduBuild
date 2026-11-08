from django.test import TestCase

from .models import Game, GenerationRequest, User


class PrototypeDatabaseTest(TestCase):
    databases = {"prototype"}

    def test_requested_schema_can_store_related_records(self):
        user = User.objects.create(
            email="teacher@example.com",
            password="django-hashed-password",
        )
        request = GenerationRequest.objects.create(
            user=user,
            grade="4",
            subject="Science",
            genre="trivia",
            difficulty="easy",
            uploaded_text="Water evaporates when heated.",
        )
        game = Game.objects.create(
            user=user,
            request=request,
            title="Water Cycle",
            game_json={"questions": []},
        )

        self.assertEqual(game.request.user, user)
        self.assertEqual(game.game_json, {"questions": []})
