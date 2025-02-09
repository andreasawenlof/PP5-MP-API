from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "display_name",
        "is_composer",
        "is_reviewer",
        "created_at",
    )


admin.site.register(Profile, ProfileAdmin)
