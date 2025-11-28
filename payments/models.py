from django.db import models
from django.utils import timezone

# Create your models here.
class Payment(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    service = models.CharField(max_length=100)
    paid_at = models.DateTimeField(default=timezone.now)
    gateway_response = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.email} - {self.service} ({self.status})"