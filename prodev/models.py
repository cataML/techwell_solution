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
    SERVICE_CHOICES = [
        ('web_dev', 'Web Development'),
        ('app_dev', 'App Development'),
        ('data_analysis', 'Data Analysis'),
        ('cloud_services', 'Cloud Services'),
        ('cybersecurity', 'Cybersecurity'),
        ('consultation', 'Consultation'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    details = models.TextField()
    status = models.CharField(max_length=30, default='Pending')  # 👈 new
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service}"

class ProdevProfile(models.Model):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('developer', 'Developer'),
    )
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="prodev_profile_user"
    )
    course_enrolled = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
#Developer dashboard
class Project(models.Model):
    STATUS_CHOICES = [
        ('ongoing','Ongoing'),
        ('completed','Completed'),
        ('pending','Pending Review')
    ]
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tech_stack = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="client_tasks") 
    status = models.CharField(max_length=50, default='pending')
    title = models.CharField(max_length=255)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_tasks")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending','Pending'), ('approved','Approved')])
    created_at = models.DateTimeField(auto_now_add=True)

#Client dashboard
class Projects(models.Model):
    STATUS_CHOICES = [
        ('ongoing','Ongoing'),
        ('completed','Completed'),
        ('pending_payment','Pending Payment')
    ]
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='project_updates')
    updated_at = models.DateTimeField(auto_now=True)

class Messages(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Projectss(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    deadline = models.DateField()
    team_members = models.IntegerField()

class Tasks(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

class MessageDev(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"
    
class ProjectOne(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)  # 'Completed', 'In Progress', 'Pending'
    team_members = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)

class TaskOne(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    profile_visibility = models.CharField(
        max_length=20,
        choices=[('public', 'Public'), ('private', 'Private')],
        default='public'
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)