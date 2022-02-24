from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionListAdmin(admin.ModelAdmin):
    list_display = ("id", "source", "target", "status", "type", "date")
    list_filter = ("type", "date", "status")
