from django.forms import ModelForm
from shop.models import Category, Product
from django import forms
from billing.models import Invoice
from shop.models import Order

class AddNewCategoryAdmin(ModelForm):
    class Meta:
        model=Category
        exclude=['slug']



class AddOrUpdateNewProductAdmin(ModelForm):
    class Meta:
        model=Product
        exclude=['created_at']



class InvoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['user', 'document_type', 'appointment', 'order', 'amount', 'description']



class StatisticsPeriodForm(ModelForm):
    class Meta:
        model = Order
        exclude=['client']
        widgets = {
            "created_at": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control"
            })
        }


