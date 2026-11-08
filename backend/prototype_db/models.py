from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


class GenerationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="generation_requests")
    grade = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    uploaded_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "generation_requests"

    def __str__(self):
        return f"{self.subject} request {self.pk}"


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    request = models.ForeignKey(
        GenerationRequest, on_delete=models.CASCADE, related_name="games"
    )
    title = models.CharField(max_length=200)
    game_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "games"

    def __str__(self):
        return self.title
