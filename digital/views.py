from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactUs, BookingNow, SignUpForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from .decorators import role_required
from .models import DigitalProfile, BookNow, Appointment, Task, Payment, Message, StaffMessage
from django.db import models


# Create your views here.
SERVICE_PRICES = {
    'government': 200,
    'tsc': 250,
    'sha_nssf': 300,
    'data_entry': 150,
    'typing': 20,
    'pdf_conversion': 100,
    'other': 100,
}

def index(request):
    return render(request, 'digital/index.html')

def about_us(request):
    return render(request, 'digital/about_us.html')

def service(request):
    return render(request, 'digital/service.html')

def blog(request):
    return render(request, 'digital/blog.html')
  

def Contact_us(request):
    if request.method == 'POST':
        form = ContactUs(request.POST)
        if form.is_valid():
            form.save()
            return redirect('digital:success_contact')
    else:
        form = ContactUs()
    return render(request, 'digital/contact_us.html', {'form' : form})

def success_contact(request):
    return render(request, "digital/success_contact.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)


            full_name = form.cleaned_data['full_name'].split(' ', 1)
            user.first_name = full_name[0]
            user.last_name = full_name[1] if len(full_name) > 1 else ''

   
            user.set_password(form.cleaned_data['password1'])
            user.save()

      
            profile, created = DigitalProfile.objects.get_or_create(user=user)
            profile.phone_number = form.cleaned_data['phone']
            profile.role = form.cleaned_data['role']
            profile.save()

            messages.success(request, "Account created successfully! Please log in.")

            return redirect('digital:log_in')
    else:
        form = SignUpForm()
    return render(request, "digital/sign_up.html", {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

          
            profile, created = DigitalProfile.objects.get_or_create(user=user)

    
            if profile.role == 'client':
                return redirect('digital:client')
            elif profile.role == 'staff':
                return redirect('digital:staff_dashboard')

            return redirect('dashboard') 
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "digital/log_in.html", {"form": form})


@login_required(login_url='/digital/log_in/')
def book_now(request):
    if request.method == 'POST':
        form = BookingNow(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user 

            service_name = booking.service.lower().replace(" ", "_").replace("/", "_")
            booking.amount = SERVICE_PRICES.get(service_name, 100)  
            booking.save()

            return redirect('payments:checkout_digital', pk=booking.pk)
    else:
        form = BookingNow()
    
    return render(request, 'digital/book_now.html', {'form': form})


@login_required(login_url='/digital/log_in/')
def confirm_booking(request, pk):
    booking = get_object_or_404(BookNow, id=pk)

    if request.method == 'POST':
        booking.status = 'paid'
        booking.save()
        return redirect('digital:client')  

    return render(request, 'digital/confirm_booking.html', {"booking": booking})

@login_required(login_url='/digital/log_in/')
def client(request):
    return render(request, 'digital/client.html')

@login_required(login_url='/digital/log_in/')
def staff(request):
    return render(request, 'digital/staff.html')

@login_required(login_url='/digital/log_in/')
@role_required(['admin', 'staff', 'cyber', 'support'])
def staff_dashboard(request):
    user = request.user

    today = timezone.localdate()
    todays_appointments = Appointment.objects.filter(date=today).count()
    pending_tasks = Task.objects.filter(done=False).count()
    payments_received = Payment.objects.filter(date__gte=today).aggregate(total=models.Sum('amount'))['total'] or 0

    appointments = Appointment.objects.filter(date__gte=today).order_by('date', 'time')[:6]
    tasks = Task.objects.filter(done=False).order_by('deadline')[:6]
    payments = Payment.objects.all()[:6]
    messages = Message.objects.filter(recipient=user).order_by('-created_at')[:6]

    context = {
        'staff_name': user.get_full_name() or user.username,
        'staff_role': getattr(user.profile, 'role', 'staff') if hasattr(user, 'profile') else 'staff',
        'todays_appointments': todays_appointments,
        'pending_tasks': pending_tasks,
        'payments_received': payments_received,
        'appointments': appointments,
        'tasks': tasks,
        'payments': payments,
        'messages': messages,
    }
    return render(request, 'digital/staff_dashboard.html', context)

def no_permission_view(request):
    return render(request, 'digital/no_permission.html')

@login_required(login_url='/digital/log_in/')
@role_required(['admin', 'staff', 'cyber', 'support'])
def staff_appointments(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'digital/staff_appointments.html', {'appointments': appointments})

@login_required(login_url='/digital/log_in/')
@role_required(['admin', 'staff', 'cyber', 'support'])
def staff_tasks(request):
    tasks = Task.objects.filter(done=False).order_by('deadline')
    return render(request, 'digital/staff_tasks.html', {'tasks': tasks})

@login_required(login_url='/digital/log_in/')
@role_required(['admin', 'staff', 'cyber', 'support'])
def staff_payments(request):
    payments = Payment.objects.all().order_by('-date')
    return render(request, 'digital/staff_payments.html', {'payments': payments})


@login_required(login_url='/digital/log_in/')
def staff_messages(request):
    messages = StaffMessage.objects.filter(staff=request.user).order_by('-date_sent')
    return render(request, 'digital/staff_messages.html', {'messages': messages})

def privacy_policy(request):
    return render(request, 'digital/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'digital/terms_conditions.html')

def our_story(request):
    return render(request, 'digital/our_story.html')

@login_required(login_url='/digital/log_in/')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("profile")  
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, "digital/profile.html", {
        "form": form,
        "profile": profile
    })

def log_out(request):
    logout(request)
    return redirect('digital:log_in')


