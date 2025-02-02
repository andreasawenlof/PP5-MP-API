from django.contrib import admin
from .models import Instrument, InstrumentCategory  # ✅ Import models


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
