from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.name} - {self.email}"

class QuoteRequest(models.Model):
    PLAN_CHOICES = [
        ("basic", "Basic Plan"),
        ("standard", "Standard Plan"),
        ("premium", "Premium Plan"),
    ]

    full_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField()
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, null=True,blank=True)
    project_details = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending Review"),
            ("reviewed", "Reviewed"),
            ("responded", "Responded"),
        ],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.full_name} - {self.get_plan_display()}"


