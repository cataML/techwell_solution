from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __srt__(self):
        return self.email


class BookNow(models.Model):
    SERVICE_CHOICES = [
        ("government", "Government Services"),
        ("tsc services", "TSC Services"),
        ("sha/ nssf services", "SHA/ NSSF Services"),
        ("data entry", "Data Entry"),
        ("typng", "Typing"),
        ("pdf conversion", "PDF Conversion"),
        ("computer lessons", "Computer Lessons"),
        ("daily pass", "Daily Pass"),
        ("monthly subscription", "Monthly Subscription"),
        ("other", "Other Online Services")
    ]


    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    

    name = models.CharField(max_length=200)
    email = models.EmailField()
    contact = models.CharField(max_length=200) 
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service} on {self.datetime}"
    

class DigitalProfile(models.Model):
    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('client', 'Client'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="digital_profile")
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')


    def __str__(self):
        return f"{self.user.username} - {self.role}"

class DigitalService(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='digital_services')
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_services')
    SERVICE_CHOICES = [
        ('government', 'Government Services'),
        ('tsc', 'TSC Services'),
        ('sha_nssf', 'SHA/NSSF Services'),
        ('data_entry', 'Data Entry'),
        ('typing', 'Typing'),
        ('pdf_conversion', 'PDF Conversion'),
        ('other', 'Other Services'),
    ]
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('upcoming', 'Upcoming'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.get_service_type_display()} for {self.client.username} on {self.date.strftime('%Y-%m-%d')}"

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('counsellor', 'Counsellor'),
        ('staff', 'Staff'),
        ('cyber', 'Cyber Team'),
        ('support', 'Support'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
class Appointment(models.Model):
    client_name = models.CharField(max_length=150)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=30, default='scheduled')  # scheduled / done / canceled
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.client_name} — {self.date} {self.time}"


class Task(models.Model):
    title = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, default='normal')  # low / normal / high
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return self.title


class Payment(models.Model):
    client_name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    method = models.CharField(max_length=50, blank=True)  # e.g. Cash, M-Pesa

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.client_name} — {self.amount}"


class Message(models.Model):
    sender = models.CharField(max_length=150)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def preview(self):
        return (self.body[:120] + '...') if len(self.body) > 120 else self.body

    def __str__(self):
        return f"Message from {self.sender}"
    
class StaffMessage(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=200)
    preview = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message to {self.staff.username}"