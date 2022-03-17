import operator
from typing import Sequence
from django.db.models import Count, Q
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from degvabank.apps.transaction.models import Transaction
from degvabank.apps.user.models import User
from degvabank.apps.account.models import Account

import matplotlib.pyplot as plt
from io import StringIO

# Transacciones fallidas/exitosas por Clientes
def generate_transaction_pdf(request=None, user=User.objects.get(username="daniel"), min_date="2020-01-01", max_date="2040-01-01"):
    success_filter = Q(status=Transaction.TransactionStatus.ACCEPTED)
    fail_filter = Q(status=Transaction.TransactionStatus.REJECTED)
    other_filter = Q(status__in=[Transaction.TransactionStatus.ERROR, Transaction.TransactionStatus.PENDING])
    transactions = {"user": user.username, "transactions": Transaction.objects.get_queryset_by_user(user).filter(date__gte=min_date, date__lte=max_date).aggregate(other=Count('id', filter=other_filter), succeed=Count('id', filter=success_filter), fail=Count('id', filter=fail_filter))}
    
    x = list(transactions["transactions"].keys())
    y = list(transactions["transactions"].values())

    transactions["transactions"]["total"] = sum(y)

    fig = plt.figure()
    plt.rcParams['svg.fonttype'] = 'none'
    if sum(y) == 0:
        plt.xticks(rotation='vertical')
        plt.xlabel("Transaction Type", labelpad=20)
        plt.ylabel("Number of Transactions", labelpad=20)
        plt.rcParams['figure.autolayout'] = True
        plt.tight_layout()
        plt.bar(x, y)
    else:
        plt.rcParams['figure.autolayout'] = True
        plt.tight_layout()
        plt.pie(y, labels=x, autopct='%.1f%%')

    plt.title('Transactions')

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
def generate_clients_pdf(request=None, min_date="2020-01-01", max_date="2040-01-01"):
    client_transactions = []

    clients = User.objects.all()
    for user in clients:
        transaction = len(Transaction.objects.get_queryset_by_user(user).filter(date__gte=min_date, date__lte=max_date))
        user = user.username
        client_transactions.append({"user": user, "transaction": transaction})

    client_transactions = sorted(client_transactions, key=lambda x: x["transaction"], reverse=True)
    x = [client_transaction["user"] for client_transaction in client_transactions]
    y = [client_transaction["transaction"] for client_transaction in client_transactions]

    fig = plt.figure()
    plt.rcParams['svg.fonttype'] = 'none'
    plt.xticks(rotation='vertical')
    plt.xlabel("Client Username", labelpad=20)
    plt.ylabel("Number of Transactions", labelpad=20)
    plt.rcParams['figure.autolayout'] = True
    plt.tight_layout()
    plt.title('Number of Transactions per Client')
    plt.bar(x, y, color=['b', 'r', 'm', 'g'])

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    svg_dta = imgdata.getvalue()

    html_string = render_to_string('./admin/generate_pdf_clients.html', {'clients_transactions': client_transactions, "svg": svg_dta})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response

# Días y horas con más transaccionalidad
def generate_date_pdf(request=None, min_date="2020-01-01", max_date="2040-01-01"):
    transactions = Transaction.objects.filter(date__gte=min_date, date__lte=max_date)
    
    transactions = transactions.values('date')
    transactions_per_date = ["20-" + transaction['date'].date().strftime("%m-%d") for transaction in transactions]
    transactions_per_time = [str(transaction['date'].hour) for transaction in transactions]

    transaction_dates = []
    dates = {*transactions_per_date}
    for date in dates:
        transaction_dates.append({"date": date, "count": transactions_per_date.count(date)})

    transaction_times = []
    times = {*transactions_per_time}
    for time in times:
        transaction_times.append({"time": time, "count": transactions_per_time.count(time)})

    transaction_times.sort(key=operator.itemgetter("time"))
    transaction_dates.sort(key=operator.itemgetter("date"))

    x = [time["time"] + ":00" for time in transaction_times]
    y = [time["count"] for time in transaction_times]

    fig = plt.figure()
    plt.rcParams['svg.fonttype'] = 'none'
    plt.xticks(rotation='vertical')
    plt.xlabel("Hours", labelpad=20)
    plt.ylabel("Number of Transactions", labelpad=20)
    plt.rcParams['figure.autolayout'] = True
    plt.tight_layout()
    plt.title('Number of Transactions per Time')
    plt.bar(x, y, color=['b', 'r', 'm', 'g'])
    

    imgtime = StringIO()
    fig.savefig(imgtime, format='svg', bbox_inches="tight")
    imgtime.seek(0)  # rewind the data

    svg_time = imgtime.getvalue()

    plt.figure().clear()
    plt.close()

    x = [date["date"] for date in transaction_dates]
    y = [date["count"] for date in transaction_dates]

    fig = plt.figure()
    plt.rcParams['svg.fonttype'] = 'none'
    plt.xticks(rotation='vertical')
    plt.xlabel("Dates", labelpad=20)
    plt.ylabel("Number of Transactions", labelpad=20)
    plt.rcParams['figure.autolayout'] = True
    plt.tight_layout()
    plt.title('Number of Transactions per Date')
    plt.bar(x, y, color=['b', 'r', 'm', 'g'])
    
    imgdate = StringIO()
    fig.savefig(imgdate, format='svg', bbox_inches="tight")
    imgdate.seek(0)  # rewind the data

    svg_date = imgdate.getvalue()

    html_string = render_to_string('./admin/generate_pdf_dates.html', {'transaction_dates': transaction_dates, 'transaction_times': transaction_times, "svg_time": svg_time, "svg_date": svg_date})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response
