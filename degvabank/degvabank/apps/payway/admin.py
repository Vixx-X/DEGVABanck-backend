from django.contrib import admin
from .models import PayWayKeys, PayWayMetaData


@admin.register(PayWayKeys)
class PayWayKeysListAdmin(admin.ModelAdmin):
    list_display = ("owner", "public")


@admin.register(PayWayMetaData)
class PayWayMetaDataListAdmin(admin.ModelAdmin):
    list_display = ("app_id", "app_name", "date_created", "user")
