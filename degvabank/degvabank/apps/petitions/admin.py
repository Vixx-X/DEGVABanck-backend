from django.contrib import admin
from .models import Petition

@admin.action(description="Mark selected petitions as approved")
def approve(modeladmin, request, queryset):
    queryset.update(status=Petition.PetitionStatus.APPROVED)

@admin.action(description="Mark selected petitions as denied")
def denied(modeladmin, request, queryset):
    queryset.update(status=Petition.PetitionStatus.DENIED)

@admin.action(description="Mark selected petitions as pending")
def pending(modeladmin, request, queryset):
    queryset.update(status=Petition.PetitionStatus.PENDING)

@admin.register(Petition)
class PetitionListAdmin(admin.ModelAdmin):
    list_display = ("id", "reason","status", "date_processed", "date_created", "user")
    list_filter = ("reason", "date_processed", "date_created", "status", "user")
    actions = [approve, denied, pending]
