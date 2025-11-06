
from django.db import models
from django.conf import settings
from django.urls import reverse
from io import BytesIO
from django.http import HttpResponse

from django.template.loader import render_to_string
from weasyprint import HTML



class Invoice(models.Model):
    DOCUMENT_TYPES = [
        ('INVOICE', 'Fattura'),
        ('QUOTE', 'Preventivo'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment = models.ForeignKey('atelier.Appointment', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey('shop.Order', on_delete=models.SET_NULL, null=True, blank=True)

    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_document_type_display()} #{self.id} - {self.user.username}"

    def get_absolute_url(self):
        return reverse('dashboard_invoice_detail', args=[self.pk])

    def generate_pdf(self):
        #Here you specify the directory of the HTML that you want to convert
        #ATTENTION with weasyprint if you're in macos like me you have to install
        #some graphic library that usally are already installed in Linux.
        #With :  brew install cairo pango gdk-pixbuf libffi 
        # and optional : brew install gtk+3
        # then reinstall weasyprint pip uninstall weasyprint pip install weasyprint
        html_string = render_to_string('dashboard/invoices/invoice_wesyprint.html', {
            'invoice': self,
        })

        buffer = BytesIO()
        HTML(string=html_string).write_pdf(buffer)
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
    


    