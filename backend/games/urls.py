"""URL routes for the game-generation API."""

from django.urls import path

from .views import generate_game

urlpatterns = [
    path("generate-game/", generate_game, name="generate-game"),
]

"""Django Template for URL routing."""