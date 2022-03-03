from django.contrib import admin
from .models import Account

# Register your models here.
@admin.register(Account)
class AccountListAdmin(admin.ModelAdmin):
    search_fields = (
        "user__username__startswith",
        "user__first_name__startswith",
        "id__startswith",
    )
    list_display = ("id", "is_active", "type", "user", "date_created")
    list_filter = ("is_active", "type", "date_created")
