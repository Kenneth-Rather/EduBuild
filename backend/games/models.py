import uuid

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Lesson(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    source_file = models.FileField(
        upload_to="lessons/%Y/%m/%d/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    source_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Game(models.Model):
    class Genre(models.TextChoices):
        TRIVIA = "trivia", "Trivia"
        PUZZLE = "puzzle", "Puzzle"
        MATCHING = "matching", "Matching"

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        GENERATING = "generating", "Generating"
        REVIEW = "review", "Ready for review"
        PUBLISHED = "published", "Published"
        FAILED = "failed", "Failed"
        ARCHIVED = "archived", "Archived"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, related_name="games")
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=20, choices=Genre.choices, default=Genre.TRIVIA)
    grade_level = models.CharField(max_length=50)
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM
    )
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class GenerationRequest(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="generation_requests")
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, related_name="generation_requests")
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="generation_requests", null=True, blank=True
    )
    settings = models.JSONField(default=dict)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.QUEUED)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Generation request {self.pk}"


class GenerationRun(models.Model):
    class Status(models.TextChoices):
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    request = models.ForeignKey(GenerationRequest, on_delete=models.CASCADE, related_name="runs")
    stage = models.CharField(max_length=50)
    attempt = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.RUNNING)
    report = models.JSONField(default=dict)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["request", "started_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["request", "stage", "attempt"],
                name="unique_generation_stage_attempt",
            )
        ]

    def __str__(self):
        return f"{self.request} - {self.stage} (attempt {self.attempt})"


class GameVersion(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        VERIFIED = "verified", "Verified"
        PUBLISHED = "published", "Published"

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="game_versions"
    )
    config = models.JSONField(default=dict)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["game", "-version_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["game", "version_number"], name="unique_game_version_number"
            )
        ]

    def __str__(self):
        return f"{self.game} v{self.version_number}"


class Question(models.Model):
    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        FLAGGED = "flagged", "Flagged"

    version = models.ForeignKey(GameVersion, on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveIntegerField()
    prompt = models.TextField()
    answer_options = models.JSONField(default=list)
    correct_answer = models.CharField(max_length=500)
    source_excerpt = models.TextField(blank=True)
    verification_status = models.CharField(
        max_length=10, choices=VerificationStatus.choices, default=VerificationStatus.PENDING
    )

    class Meta:
        ordering = ["version", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["version", "order"], name="unique_question_order_per_version"
            )
        ]

    def __str__(self):
        return f"Question {self.order} for {self.version}"


class ShareLink(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="share_links")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Share link for {self.game}"
