# atelier/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

OPENING_HOURS = {
    "morning_start": 9,
    "morning_end": 13,
    "afternoon_start": 15,
    "afternoon_end": 19,
}


class Appointment(models.Model):
    activity = models.CharField(max_length=255)
    date = models.DateTimeField()
    duration = models.DurationField()
    extra_note = models.TextField(null=True, blank=True)

    is_completed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    new_measurements_head = models.PositiveIntegerField(null=True, blank=True)
    new_measurements_chest = models.PositiveIntegerField(null=True, blank=True)
    new_measurements_waist = models.PositiveIntegerField(null=True, blank=True)
    new_measurements_hips = models.PositiveIntegerField(null=True, blank=True)
    new_measurements_sleeve = models.PositiveIntegerField(null=True, blank=True)

    client = models.ForeignKey("users.Client", on_delete=models.CASCADE, related_name="appointments")

    def __str__(self):
        return f"{self.client} - {self.activity} ({self.date.date()})"

    def clean(self):
        """Validazione dell'appuntamento (orario e sovrapposizioni)"""
        if not self.client_id:
            return  # evita l'errore durante i test o i salvataggi parziali

        if self.date is None or self.duration is None:
            return

        if not (
            OPENING_HOURS["morning_start"] <= self.date.hour < OPENING_HOURS["morning_end"]
            or OPENING_HOURS["afternoon_start"] <= self.date.hour < OPENING_HOURS["afternoon_end"]
        ):
            raise ValidationError("Prenotazione fuori orario di apertura.")

        if self.date < timezone.now():
            raise ValidationError("Non puoi prenotare nel passato.")

        start_time = self.date
        end_time = self.date + self.duration

        overlapping = Appointment.objects.filter(
            client=self.client,
            date__lt=end_time,
            date__gte=start_time - timedelta(hours=2)
        ).exclude(pk=self.pk)

        for app in overlapping:
            app_end = app.date + app.duration
            if app.date < end_time and app_end > start_time:
                raise ValidationError("Esiste già un appuntamento in questo orario.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class MeasurementHistory(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    head = models.PositiveIntegerField(null=True, blank=True)
    chest = models.PositiveIntegerField(null=True, blank=True)
    waist = models.PositiveIntegerField(null=True, blank=True)
    hips = models.PositiveIntegerField(null=True, blank=True)
    sleeve = models.PositiveIntegerField(null=True, blank=True)

    #FK
    client = models.ForeignKey("users.Client", on_delete=models.CASCADE, related_name="measurements")

    def __str__(self):
        return f"Measurement for {self.client} on {self.date.date()}"