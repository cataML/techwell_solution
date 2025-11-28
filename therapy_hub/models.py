from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.name} - {self.email}"

class Booking(models.Model):

    SERVICE_CHOICES = [
        ('individual therapy', 'Individual Therapy'),
        ('couples therapy', 'Couples Therapy'),
        ('corporate therapy', 'Corporate Therapy'),
        ('basic plan', 'Basic Plan'),
        ('standard plan', 'Standard Plan'),
        ('premium plan', 'Premium Plan')
    ]

    SESSION_CHOICES = [
        ('virtual', 'Virtual Session'),
        ('in_person', 'In-person Session'),
        ('group', 'Group Session'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    client_name = models.CharField(max_length=100, null=True, blank=True)

    session_type = models.CharField(
        max_length=100,
        choices=[
            ('individual', 'Individual'),
            ('couples', 'Couples'),
            ('corporate', 'Corporate'),
        ],
        default='individual'
    )
  
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, blank=True)
    session = models.CharField(max_length=100, choices=SESSION_CHOICES, blank=True)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.session_type:
            self.session_type = self.session_type.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.service} on {self.date}"

class Profile(models.Model):
    ROLE_CHOICES = (
        ('counsellor', 'Counsellor'),
        ('client', 'Client'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="therapy_profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Session(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='counselor_sessions')
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(
        max_length=20,
        choices=[('completed', 'Completed'), ('upcoming', 'Upcoming')],
        default='upcoming'
    )

    def __str__(self):
        return f"Session {self.id} with {self.client.username} on {self.date.strftime('%Y-%m-%d')}"
    
class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('counsellor', 'Counsellor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='therapy_users',  # prevent clash with auth.User
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='therapy_users_permissions',  # prevent clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )