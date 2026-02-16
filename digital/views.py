from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactUs, BookingNow, SignUpForm, UserForm, ClientProfileForm, ClientSettingsForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import messages as django_messages
from django.utils import timezone
from .decorators import role_required
from .models import DigitalProfile, BookNow, Appointment, Task, Payment, Message, ClientProfile, Booking, ClientPayment, DigitalServices, DigitalBlog, DigitalTeam
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
SERVICE_PRICES = {
    'government': 200,
    'tsc': 250,
    'sha_nssf': 300,
    'data_entry': 500,
    'typing': 100,
    'pdf_conversion': 1,
    'daily_pass': 300,
    'monthly_subscription': 4500,
    'computer_lessons': 3000,
    'other': 100,
}

def index(request):
    
    return render(request, 'digital/index.html')

def about_us(request):
    team_members = DigitalTeam.objects.filter(is_active=True)
    return render(request, 'digital/about_us.html',{
        'team_members': team_members
    })

def service(request):
    services = DigitalServices.objects.filter(is_active=True)
    return render(request, 'digital/service.html',{
        'services' : services
    })

def blog(request):
    blogs = DigitalBlog.objects.all().order_by('-date')
    return render(request, 'digital/blog.html', {
        'blogs': blogs})
  

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
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            DigitalProfile.objects.get_or_create(user=user)

            # 🔑 KEY LINE
            if next_url:
                return redirect(next_url)

            return redirect('digital:dashboard')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "digital/log_in.html", {
        "form": form,
        "next": next_url
    })

def log_out(request):
    logout(request)
    return redirect('digital:log_in')

def book_now(request):
    if request.method == 'POST':
        form = BookingNow(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            booking.client = request.user if request.user.is_authenticated else None

            service_key = (
                booking.service.lower()
                .replace(" ", "_")
                .replace("/", "_")
            )

            booking.amount = SERVICE_PRICES.get(
                service_key,
                SERVICE_PRICES['other']
            )

            booking.save()
            return redirect('digital:guest', pk=booking.pk)

    else:
        form = BookingNow()

    return render(request, 'digital/book_now.html', {'form': form})

def choose_login_or_guest(request, pk):
    booking = BookNow.objects.get(pk=pk)
    return render(request, 'digital/guest.html', {'booking': booking})

@login_required(login_url='/digital/log_in/')
def confirm_booking(request, pk):
    booking = get_object_or_404(BookNow, id=pk)

    if request.method == 'POST':
        booking.status = 'paid'
        booking.save()
        return redirect('digital:client')  

    return render(request, 'digital/confirm_booking.html', {"booking": booking})

@login_required(login_url='/digital/log_in/')
def dashboard(request):
    return render(request, 'digital/dashboard.html')

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
    tasks = Task.objects.filter(assigned_to=user, done=False).order_by('deadline')[:6]
    payments = Payment.objects.all()[:6]
    user_messages = Message.objects.filter(recipient=user).order_by('-date_sent')[:6]

    context = {
        'staff_name': user.get_full_name() or user.username,
        'staff_role': getattr(user.profile, 'role', 'staff') if hasattr(user, 'profile') else 'staff',
        'todays_appointments': todays_appointments,
        'pending_tasks': pending_tasks,
        'payments_received': payments_received,
        'appointments': appointments,
        'tasks': tasks,
        'payments': payments,
        'messages': user_messages,
    }
    return render(request, 'digital/staff_dashboard.html', context)

def no_permission_view(request):
    return render(request, 'digital/no_permission.html')

@login_required(login_url='/digital/log_in/')
@role_required(['admin', 'staff', 'cyber', 'support'])
def staff_appointments(request):
    # All scheduled appointments assigned to this staff
    appointments = Appointment.objects.filter(
        staff=request.user,
        status='scheduled'
    )

    # Appointments for this staff that are not completed
    appt = Appointment.objects.filter(
        staff=request.user,
    ).exclude(status='completed')

    context = {
        "staff_name": request.user.get_full_name() or request.user.username,
        "staff_role": "staff",
        "appointments": appointments,
        "todays_appointments": appointments.filter(
            date=timezone.now().date()
        ).count(),
        "pending_appointments": appt.count(),
        "appt": appt,
    }

    return render(request, "digital/staff_appointments.html", context)

@login_required(login_url='/digital/log_in/')
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        staff=request.user
    )

    if appointment.status == 'completed':
        return redirect('digital:staff_dashboard')

    appointment.status = 'completed'
    appointment.completed_at = timezone.now()
    appointment.save()

    return redirect('digital:staff_dashboard')

@login_required(login_url='/digital/log_in/')
def completed_appointments(request):
    appointments = Appointment.objects.filter(
        staff=request.user,
        status='completed'
    ).order_by('-completed_at')

    return render(
        request,
        "digital/staff_completed_appointments.html",
        {"appointments": appointments}
    )

@login_required(login_url='/digital/log_in/')
@role_required(['admin', 'staff', 'cyber', 'support'])
def staff_tasks_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-deadline')
    pending_count = tasks.filter(done=False).count()  
    context = {
        "tasks": tasks,
        "staff_role": "staff",
        "pending_count": pending_count,
    }
    return render(request, "digital/staff_tasks.html", context)


@login_required
def mark_task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    response = {"success": False, "pending_count": 0}

    if request.method == "POST" and not task.done:
        task.done = True
        task.completed_at = timezone.now()
        task.save()
        pending_count = Task.objects.filter(assigned_to=request.user, done=False).count()
        response["success"] = True
        response["pending_count"] = pending_count

    return JsonResponse(response)


@login_required(login_url='/digital/log_in/')
@role_required(['admin', 'staff', 'cyber', 'support'])
def staff_payments(request):
    payments = Payment.objects.all().order_by('-date')
    return render(request, 'digital/staff_payments.html', {'payments': payments})



@login_required
def messages_view(request):
    if request.method == "POST":
        recipient_id = request.POST.get("recipient")
        text = request.POST.get("message")

        recipient = User.objects.get(id=recipient_id)

        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            message=text
        )

        return redirect('digital:messages')

    messages = Message.objects.filter(
        recipient=request.user
    ).order_by('-date_sent')

    clients = User.objects.filter(profile__role="client")  # adjust if you use role field

    return render(request, 'digital/messages.html', {
        'messages': messages,
        'clients': clients
    })

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    conversation = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('date_sent')

    if request.method == "POST":
        text = request.POST.get("message")

        if text:
            Message.objects.create(
                sender=request.user,
                recipient=other_user,
                message=text
            )

    context = {
        "conversation": conversation,
        "other_user": other_user
    }

    return render(request, "digital/chat.html", context)
@login_required
def inbox(request):
    messages = Message.objects.filter(
        recipient=request.user
    ).select_related('sender')

    context = {
        'messages': messages
    }

    return render(request, 'digital/inbox.html', context)
@login_required(login_url='/digital/log_in/')


def privacy_policy(request):
    return render(request, 'digital/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'digital/terms_conditions.html')

def our_story(request):
    return render(request, 'digital/our_story.html')




@login_required
def profile_view(request):
    profile, created = DigitalProfile.objects.get_or_create(user=request.user)

    context = {'profile': profile}
    return render(request, 'digital/update_profile.html', context)

@login_required
def edit_profile(request):
    # Ensure the user's DigitalProfile exists
    profile, created = DigitalProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('digital:update_profile') 
    else:
        form = ClientProfileForm(instance=profile)

    return render(request, 'digital/edit_profile.html', {'form': form})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    context = {
        'bookings': bookings
    }
    return render(request, 'digital/my_bookings.html', context)

@login_required(login_url='/digital/log_in/')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been cancelled.')
    else:
        messages.error(request, f'Booking #{booking.id} cannot be cancelled.')

    return redirect('my_bookings')

@login_required(login_url='/digital/log_in/')
def client_payments(request):
    payments = ClientPayment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'digital/client_payments.html', {'payments': payments})

@login_required(login_url='/digital/log_in/')
def user_messages_view(request):
    user_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'digital/messages.html', {'messages': user_messages})

@login_required(login_url='/digital/log_in/')
@role_required(['client'])
def client_messages(request):

    # Fetch messages sent TO this client
    messages = Message.objects.filter(
        recipient=request.user
    ).order_by('-date_sent')

    # Get staff users (adjust role field if needed)
    staff_users = User.objects.filter(
        profile__role__in=['staff', 'admin']   # change if your role field is different
    )

    # Handle sending message
    if request.method == "POST":
        recipient_id = request.POST.get("recipient")
        message_text = request.POST.get("message")

        if recipient_id and message_text:
            recipient = get_object_or_404(User, id=recipient_id)

            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                message=message_text
            )

            django_messages.success(request, "Message sent successfully!")
            return redirect('digital:client_messages')

    context = {
        "messages": messages,
        "staff_users": staff_users,
    }

    return render(request, "digital/client_messages.html", context)

@login_required
def settings_view(request):
    profile, created = DigitalProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        settings_form = ClientSettingsForm(request.POST, instance=profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if "save_settings" in request.POST and settings_form.is_valid():
            settings_form.save()
            messages.success(request, "Settings updated successfully!")
            return redirect('digital:settings')

        if "change_password" in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keeps user logged in
            messages.success(request, "Password changed successfully!")
            return redirect('digital:settings')
    else:
        settings_form = ClientSettingsForm(instance=profile)
        password_form = PasswordChangeForm(user=request.user)

    context = {
        "settings_form": settings_form,
        "password_form": password_form,
    }
    return render(request, "digital/settings.html", context)