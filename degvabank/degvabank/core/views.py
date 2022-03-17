from django.views.generic.edit import FormView
from degvabank.core import forms
from degvabank.apps.user.generate_pdfs import generate_transaction_pdf, generate_clients_pdf

class BaseAdminReportView(FormView):

    template_name = "admin/admin_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["admin_form"] = ctx["form"]
        return ctx

class ReportClientTransaction(BaseAdminReportView):

    form_class = forms.TransactionForm

    def form_valid(self, form):
        data = form.cleaned_data
        print("HOLA")
        return generate_transaction_pdf(user=data["user"], min_date=data["min_date"], max_date=data["max_date"])

class ReportClientList(BaseAdminReportView):

    form_class = forms.ReportForm

    def form_valid(self, form):
        data = form.cleaned_data
        return generate_clients_pdf(min_date=data["min_date"], max_date=data["max_date"])

class ReportTransactions(BaseAdminReportView):

    form_class = forms.ReportForm

    def form_valid(self, form):
        # retorna tu pdf tal cual lo habias hecho
        return super().form_valid(form)
