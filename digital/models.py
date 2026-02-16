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
    amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} on {self.date} from {self.start_time} to {self.end_time}"
    

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
    profile_picture = models.ImageField( upload_to='profile_pics/', blank=True, null=True)

    theme = models.CharField(max_length=50, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    language = models.CharField(max_length=50, choices=[('English', 'English'), ('Spanish', 'Spanish'), ('French', 'French')], default='English')
    country = models.CharField(max_length=100, 
    choices=[('Kenya', 'Kenya'), ('USA', 'USA'), ('UK', 'UK'), ('Other', 'Other')], default='Kenya')
    
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
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client_name = models.CharField(max_length=100)

    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.client_name} - {self.date}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    ]

    title = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    deadline = models.DateField(blank=True, null=True)
    done = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['done', 'deadline', '-created_at']

    def __str__(self):
        return f"{self.title} ({'Done' if self.done else 'Pending'})"

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
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages', 
    )
    message = models.TextField(default="Hello")
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_sent']   # important for chat flow

    def __str__(self):
        return f"{self.sender} → {self.recipient}"
    
    
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100, blank=True)
    last_name=models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=100, null=True)
    date = models.DateField()
    time = models.TimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.service}"

class ClientPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)  # e.g., Cash, Card, Mpesa
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    booking = models.ForeignKey('Booking', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.user.username}"


#Services model
class DigitalServices(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    image = models.URLField()
    items = models.TextField(
        help_text="Enter one item per line (bullet points)",
        default="Not specified"
    )
    is_active = models.BooleanField(default=True)

    def item_list(self):
        return self.items.splitlines()

    def __str__(self):
        return self.title
#Team model
class DigitalTeam(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='team/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
#Blog model
class DigitalBlog(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    date = models.DateField()
    image = models.URLField()
    full_content = models.TextField(help_text="You can use HTML for lists and paragraphs")

    def __str__(self):
        return self.title