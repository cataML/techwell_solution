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
    phone = models.CharField(max_length=20, null=True, blank=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, null=True, blank=True)
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

#Services model
class ProdevService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    items = models.TextField(
        help_text="Enter bullet points, one per line"
    )
    is_active = models.BooleanField(default=True)

    def item_list(self):
        return self.items.splitlines()

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tools_used = models.CharField(max_length=255)
    outcome = models.TextField()
    image = models.ImageField(upload_to="projects/")
    github_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    page = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title