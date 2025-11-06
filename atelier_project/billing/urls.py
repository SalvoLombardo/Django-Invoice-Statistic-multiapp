# billing/urls.py
from django.urls import path
from .views import download_invoice_pdf

urlpatterns = [
    path('invoice/<int:pk>/pdf/', download_invoice_pdf, name='download_invoice_pdf'),
]