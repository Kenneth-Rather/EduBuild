"""Django application configuration for game generation."""

from django.apps import AppConfig


class GamesConfig(AppConfig):
    """Tell Django how to identify and load the game-generation app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "games"
