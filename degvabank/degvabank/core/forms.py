from django import forms
from degvabank.apps.user.models import User

class ReportForm(forms.Form):
    min_date = forms.fields.DateField(label='Start Date', widget=forms.SelectDateWidget)
    max_date = forms.DateField(label='End Date', widget=forms.SelectDateWidget)

class TransactionForm(ReportForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
