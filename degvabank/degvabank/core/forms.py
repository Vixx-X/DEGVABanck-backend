from datetime import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from degvabank.apps.user.models import User

class ReportForm(forms.Form):
    # lo inicio un mes atras
    min_date = forms.DateField(label='Start Date', widget=forms.SelectDateWidget)
    # lo inicio con la fecha actual
    max_date = forms.DateField(label='End Date', widget=forms.SelectDateWidget)

class TransactionForm(ReportForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
