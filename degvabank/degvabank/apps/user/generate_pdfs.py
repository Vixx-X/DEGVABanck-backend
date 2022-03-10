from itertools import count
import operator
from django.db.models import Count, Q
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML

from degvabank.apps.transaction.models import Transaction
from degvabank.apps.user.models import User
from degvabank.apps.account.models import Account

import matplotlib.pyplot as plt
from io import StringIO
from matplotlib import numpy as np

# Transacciones fallidas/exitosas por Clientes
def generate_transaction_pdf(request=None, user=User.objects.get(username="daniel")):    
    success_filter = Q(status=Transaction.TransactionStatus.ACCEPTED)
    fail_filter = Q(status=Transaction.TransactionStatus.REJECTED)
    transactions = {"user": user.username, "transactions": Transaction.objects.get_queryset_by_user(user).aggregate(other=Count('id', filter=~(success_filter&fail_filter)), succeed=Count('id', filter=success_filter), fail=Count('id', filter=fail_filter))}
    
    x = transactions["transactions"].keys()
    y = transactions["transactions"].values()

    transactions["transactions"]["total"] = sum(y)

    fig = plt.figure()
    plt.pie(y, labels=x)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    svg_dta = imgdata.getvalue()  # this is svg data

    html_string = render_to_string('./admin/generate_pdf_transaction.html', {'transactions': transactions, "svg": svg_dta})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response


# Clientes ordenados por cantidad de transacciones
def generate_clients_pdf(request=None):
    transactions = Transaction.objects.all()

    clients = User.objects.all()
    clients_transactions = []

    for client in clients:
        clients_accounts = Account.objects.filter(user=client)
        client_transactions = []

        for account in clients_accounts:
            transaction = transactions.filter(target=account.id)
            if (len(transaction)):
                client_transactions.append(transaction)
            transaction = transactions.filter(source=account.id)
            if (len(transaction)):
                client_transactions.append(transaction)

        clients_transactions.append({"user": client.username, "num_transactions": len(client_transactions)})

    clients_transactions.sort(key=operator.itemgetter("num_transactions"))
    clients_transactions.reverse()

    html_string = render_to_string('./admin/generate_pdf_clients.html', {'clients_transactions': clients_transactions})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response

# Días y horas con más transaccionalidad
def generate_date_pdf(request=None):
    transactions = Transaction.objects.all()
    
    transactions = transactions.values('date')
    transactions_per_date = [str(transaction['date'].date()) for transaction in transactions]
    transactions_per_time = [str(transaction['date'].hour) for transaction in transactions]

    transaction_dates = []
    dates = {*transactions_per_date}
    for date in dates:
        transaction_dates.append({"date": date, "count": transactions_per_date.count(date)})

    transaction_times = []
    times = {*transactions_per_time}
    for time in times:
        transaction_times.append({"time": time, "count": transactions_per_time.count(time)})

    transaction_times.sort(key=operator.itemgetter("count"))
    transaction_times.reverse()
    transaction_dates.sort(key=operator.itemgetter("count"))
    transaction_dates.reverse()

    html_string = render_to_string('./admin/generate_pdf_dates.html', {'transaction_dates': transaction_dates, 'transaction_times': transaction_times})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response
