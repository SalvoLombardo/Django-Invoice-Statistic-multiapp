# dashboard/models.py
from django.db import models


class SystemLog(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)

    #FK
    user = models.ForeignKey("users.Client", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action}"