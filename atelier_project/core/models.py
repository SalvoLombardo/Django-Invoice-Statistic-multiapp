# core/models.py
from django.db import models


class StoreInfo(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    about_text = models.TextField(blank=True)

    def __str__(self):
        return self.name