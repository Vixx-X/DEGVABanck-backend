from django.views.generic.edit import FormView

from degvabank.core import forms


class BaseAdminReportView(FormView):

    template_name = "admin/admin_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["admin_form"] = ctx["form"]
        return ctx

class ReportClientTransaction(BaseAdminReportView):

    form_class = forms.Form

    def form_valid(self, form):
        # retorna tu pdf tal cual lo habias hecho
        return super().form_valid(form)

class ReportClientList(BaseAdminReportView):

    form_class = forms.Form

    def form_valid(self, form):
        # retorna tu pdf tal cual lo habias hecho
        return super().form_valid(form)

class ReportTransactions(BaseAdminReportView):

    form_class = forms.Form

    def form_valid(self, form):
        # retorna tu pdf tal cual lo habias hecho
        return super().form_valid(form)
