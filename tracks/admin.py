from django.contrib import admin
from .models import Track, Genre, Mood, ProjectType


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "genre", "mood",
                    "project_type", "updated_at")
    list_filter = ("status", "genre", "mood", "project_type")
    search_fields = ("title", "notes")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
