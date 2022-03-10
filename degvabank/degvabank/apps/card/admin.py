from django.contrib import admin
from .models import CreditCard, DebitCard

@admin.register(CreditCard)
class CreditCardListAdmin(admin.ModelAdmin):
    search_fields = (
        "user__username__startswith",
        "user__first_name__startswith",
        "number__startswith",
    )
    list_display = ("number", "expiration_date", "is_active", "credit", "credit_limit", "user", "date_created")
    list_filter = ("expiration_date", "credit", "date_created", "is_active")

@admin.register(DebitCard)
class DebitCardListAdmin(admin.ModelAdmin):
    search_fields = (
        "account__id__startswith",
        "account__user__username__startswith",
        "account__user__first_name__startswith",
        "number__startswith",
    )
    list_display = ("number", "expiration_date", "is_active", "date_created", "account")
    list_filter = ("expiration_date", "date_created", "is_active")
