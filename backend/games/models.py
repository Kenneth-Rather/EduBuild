from django.db import models

class GameRecord(models.Model):
    username = models.CharField(max_length=150)
    game_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username} - {self.game_name}"