from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from degvabank.apps.transaction.models import Transaction

def html_to_pdf_view(request):
    transactions = Transaction.objects.all()
    html_string = render_to_string('./admin/generate_pdf_transaction.html', {'transactions': transactions})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response
