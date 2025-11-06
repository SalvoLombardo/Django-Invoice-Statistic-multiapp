from django.forms import ModelForm
from django import forms


from .models import Category,Product, Cart, CartItem, Order, OrderItem, Payment


class ChangeCartStatus(ModelForm):
    class Meta:
        model= Cart
        fields=['is_active']

class HowManyItemsInTheCart(ModelForm):
    class Meta:
        model= CartItem
        fields=['quantity']



class ChangeOrderStatus(ModelForm):
    class Meta:
        model=Order
        fields=['status']


class PaymentExecuted(ModelForm):
    class Meta:
        model=Payment
        fields=['method','is_successful']




####FORM for Statistics




class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Da"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="A"
    )