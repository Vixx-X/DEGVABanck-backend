from itertools import count
import operator
from django.db.models import Count
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from degvabank.apps.transaction.models import Transaction
from degvabank.apps.user.models import User
from degvabank.apps.account.models import Account

def get_filter_transactions(type=None, status=None, amount=None, 
    max_amount=None, min_amount=None, reason=None, date=None, min_date=None, max_date=None,
    target=None, source=None):
    transactions = Transaction.objects.all()

    if(type):
        transactions = transactions.filter(type=type)

    if(status):
        transactions = transactions.filter(status=status)

    if(amount):
        transactions = transactions.filter(amount=amount)
    else:
        if(min_amount):
            transactions = transactions.filter(amount__gte=min_amount)

        if(max_amount):
            transactions = transactions.filter(amount__lte=max_amount)

    if(reason):
        transactions = transactions.filter(reason__icontains=reason)

    if(date):
        transactions = transactions.filter(date=date)
    else:
        if(min_date):
            transactions = transactions.filter(date__gte=min_date)

        if(max_date):
            transactions = transactions.filter(date__lte=max_date)

    if(target):
        transactions = transactions.filter(target=target)
    
    if(source):
        transactions = transactions.filter(source=source)

    return transactions

# Transacciones fallidas/exitosas por Clientes
def generate_transaction_pdf(request=None, type=None, status=None, amount=None, 
    max_amount=None, min_amount=None, reason=None, date=None, min_date=None, max_date=None,
    target=None, source=None):
    transactions = get_filter_transactions(type=type, status=status, amount=amount, 
                    max_amount=max_amount, min_amount=min_amount, reason=reason, date=date, min_date=min_date, max_date=max_date,
                    target=target, source=source)


    html_string = render_to_string('./admin/generate_pdf_transaction.html', {'transactions': transactions})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response


# Clientes ordenados por cantidad de transacciones
def generate_clients_pdf(request=None, type=None, status=None, amount=None, 
    max_amount=None, min_amount=None, reason=None, date=None, min_date=None, max_date=None,
    target=None, source=None):
    transactions = get_filter_transactions(type=type, status=status, amount=amount, 
                    max_amount=max_amount, min_amount=min_amount, reason=reason, date=date, min_date=min_date, max_date=max_date,
                    target=target, source=source)

    clients = User.objects.filter(type=User.UserType.JURIDIC)
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
def generate_date_pdf(request=None, type=None, status=None, amount=None, 
    max_amount=None, min_amount=None, reason=None, date=None, min_date=None, max_date=None,
    target=None, source=None):
    transactions = get_filter_transactions(type=type, status=status, amount=amount, 
                    max_amount=max_amount, min_amount=min_amount, reason=reason, date=date, min_date=min_date, max_date=max_date,
                    target=target, source=source)
    
    transactions_per_date = transactions.values('date').annotate(count=Count('date')).order_by('date')

    html_string = render_to_string('./admin/generate_pdf_dates.html', {'transactions': transactions_per_date})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response
