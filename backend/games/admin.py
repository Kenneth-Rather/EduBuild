from django.contrib import admin

from .models import (
    Game,
    GameVersion,
    GenerationRequest,
    GenerationRun,
    Lesson,
    Question,
    ShareLink,
)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "created_at")
    search_fields = ("title", "owner__username")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "genre", "status", "updated_at")
    list_filter = ("genre", "difficulty", "status")
    search_fields = ("title", "owner__username")


@admin.register(GenerationRequest)
class GenerationRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "lesson", "requested_by", "status", "created_at")
    list_filter = ("status",)


@admin.register(GenerationRun)
class GenerationRunAdmin(admin.ModelAdmin):
    list_display = ("request", "stage", "attempt", "status", "started_at")
    list_filter = ("status", "stage")


@admin.register(GameVersion)
class GameVersionAdmin(admin.ModelAdmin):
    list_display = ("game", "version_number", "status", "created_at")
    list_filter = ("status",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("version", "order", "verification_status")
    list_filter = ("verification_status",)
    search_fields = ("prompt", "source_excerpt")


@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ("game", "token", "is_active", "created_at", "expires_at")
    list_filter = ("is_active",)
