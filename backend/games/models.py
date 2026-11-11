from django.db import models

"""Models for tracking generated games."""
"""written by Dylan, with aid in Django DB Models doc"""
class GameRecord(models.Model):
    username = models.CharField(max_length=150)
    game_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username} - {self.game_name}"