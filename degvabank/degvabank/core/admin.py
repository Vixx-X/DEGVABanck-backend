from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig
from django.urls import path

from degvabank.core import views

class CustomAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                'reports/client_transaction/',
                self.admin_view(views.ReportClientList.as_view()),
                name='report-client-transaction',
            ),
            path(
                'reports/client_list/',
                self.admin_view(views.ReportClientList.as_view()),
                name='report-client-list',
            ),
            path(
                'reports/transactions/',
                self.admin_view(views.ReportTransactions.as_view()),
                name='report-transactions',
            ),
        ]
        urls = my_urls + urls
        return urls


class AdminConfig(AdminConfig):
    default_site = "degvabank.core.admin.CustomAdminSite"
