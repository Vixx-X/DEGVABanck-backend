"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'degvabank.menu.CustomMenu'
"""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for DEGVABank-backend admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*', "degvabank.apps.user.*")
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*', "degvabank.apps.user.*")
            ),
            items.MenuItem(
                _('Reports'),
                children=[
                    items.MenuItem(
                        _("Client Transactions"),
                        reverse('admin:report-client-transaction')
                    ),
                    items.MenuItem(
                        _("Client list"),
                        reverse('admin:report-client-list')
                    ),
                    items.MenuItem(
                        _("Transactions"),
                        reverse('admin:report-transactions')
                    ),
                ]
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
