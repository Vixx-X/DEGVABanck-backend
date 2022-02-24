from django.contrib import admin
from .models import PayWayKeys

@admin.register(PayWayKeys)
class TransactionListAdmin(admin.ModelAdmin):
    list_display = ("owner", "public")

