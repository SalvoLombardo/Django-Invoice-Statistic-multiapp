from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client



#Questo Form eredita da UserCreationForm e i campi sotto
# ovvero first_name, last_name,email sono già dentro il modello User
# modello di default di Django
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

# Form per il Client (profilo extra)
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("user",)  # user sarà associato nella view



