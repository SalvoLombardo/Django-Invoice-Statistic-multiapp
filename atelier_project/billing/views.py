# billing/views.py
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Invoice

@login_required
def download_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    return invoice.generate_pdf()