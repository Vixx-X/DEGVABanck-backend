from django.contrib import admin
from .models import Account

# Register your models here.
@admin.register(Account)
class AccountListAdmin(admin.ModelAdmin):
    search_fields = ("user__username__startswith", "user__first_name__startswith", "id__startswith")
    list_display = ("id", "status", "type", "user", "creation_date")
    list_filter = ("status", "type", "creation_date")
