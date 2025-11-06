from django.forms import ModelForm
from django import forms
from datetime import timedelta
from .models import Appointment

from .models import Appointment, MeasurementHistory

class NewAppointmentFormAdmin(ModelForm):
    class Meta:
        model= Appointment
        fields= '__all__'


    
class AppointmentStatusAdmin(ModelForm):
    class Meta:
        model=Appointment
        fields= ['is_completed','is_paid']



class BookAppointmentUserForm(forms.ModelForm):
    DURATION_CHOICES = [
        (timedelta(minutes=30), "30 minuti"),
        (timedelta(hours=1), "1 ora"),
        (timedelta(hours=1, minutes=30), "1 ora e 30 minuti"),
    ]

    duration_choice = forms.ChoiceField(
        choices=[(str(k), v) for k, v in DURATION_CHOICES],
        label="Durata",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Appointment
        fields = ["activity", "date", "duration_choice", "extra_note"]
        widgets = {
            "activity": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Descrivi l'attività (es. prova abito, consegna, misurazione)"
            }),
            "date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control"
            }),
            "extra_note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Note aggiuntive (facoltative)"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        duration_str = cleaned_data.get("duration_choice")
        if duration_str:
            # Convertiamo la stringa di timedelta in oggetto timedelta
            hours, minutes, seconds = map(float, duration_str.replace("day, ", "").split(":"))
            cleaned_data["duration"] = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.duration = self.cleaned_data["duration"]
        if commit:
            instance.save()
        return instance


class NewMesurementAdmin(ModelForm):
    class Meta:
        model= MeasurementHistory
        exclude=['date']




class NewMesurementUser(ModelForm):
    class Meta:
        model= MeasurementHistory
        exclude=['client','date']



    
        