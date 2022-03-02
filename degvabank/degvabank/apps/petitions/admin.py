from django.contrib import admin
from .models import Petition

@admin.register(Petition)
class PetitionListAdmin(admin.ModelAdmin):
    list_display = ("id", "reason","status", "date_processed", "date_created", "user")
    list_filter = ("reason", "date_processed", "date_created", "status", "user")
