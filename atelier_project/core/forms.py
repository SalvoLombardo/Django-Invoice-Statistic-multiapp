from django.forms import ModelForm
from .models import StoreInfo

class AddInfo(ModelForm):
    class Meta:
        model=StoreInfo
        fields='__all__'