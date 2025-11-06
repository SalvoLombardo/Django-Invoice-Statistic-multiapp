# users/models.py
from django.db import models
from django.contrib.auth.models import User


class Role(models.TextChoices):
    CLIENT = "CLIENT", "Client"
    SARTA = "SARTA", "Sarta"
    ADMIN = "ADMIN", "Admin"


class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'
    

class Client(models.Model):
    
    #Stile enum
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)

    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    # misure base
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.FEMALE)   
    measurements_head = models.PositiveIntegerField(null=True, blank=True)
    measurements_chest = models.PositiveIntegerField(null=True, blank=True)
    measurements_waist = models.PositiveIntegerField(null=True, blank=True)
    measurements_hips = models.PositiveIntegerField(null=True, blank=True)
    measurements_sleeve = models.PositiveIntegerField(null=True, blank=True)

    #FK speciale di Django che punta ad una tabella aggiuntiva creata da Django stesso (auth_user)
    #Quindi la nostra tabella users.Client(nomeapp.nomemodello) punta ad auth_user creata da Djago che 
    #contiente username, password (almeno, poi si possono aggiungere altri campi)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.role})"

    def measurement_summary(self):
        return (
            f"Head: {self.measurements_head}, Chest: {self.measurements_chest}, "
            f"Waist: {self.measurements_waist}, Hips: {self.measurements_hips}, "
            f"Sleeve: {self.measurements_sleeve}"
        )








    