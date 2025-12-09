from django.shortcuts import render, redirect
from .forms import ContactForm, BookingForm, SignUpForm
from django.contrib.auth import login, logout
from .models import Profile, Booking, Session, Payment 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Sum



# Create your views here.
def index(request):
    return render(request, 'therapy_hub/index.html')

def about(request):
    return render(request, 'therapy_hub/about.html')

def services(request):
    return render(request, 'therapy_hub/services.html')

def contact(request):
    return render(request, 'therapy_hub/contact.html')

def contact_view(request, template_name="therapy_hub/contact.html"):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() 
            return render(request, 'therapy_hub/success_contact.html')  

    else:
        form = ContactForm()
    return render(request, template_name, {'form': form})


def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = "pending"
            booking.save()
           
            base_url = reverse('payments:checkout_therapy', kwargs={'pk': booking.id})
            query_string = urlencode({'source': 'therapy_hub'})
            url = f"{base_url}?{query_string}"
            return HttpResponseRedirect(url)
    else:
        form = BookingForm()
    return render(request, 'therapy_hub/booking.html', {'form': form})

def case_study(request):
    return render(request, 'therapy_hub/case_study.html')

def events(request):
    return render(request, 'therapy_hub/events.html')

def courses(request):
    return render(request, 'therapy_hub/courses.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)


            full_name = form.cleaned_data['full_name'].split(' ', 1)
            user.first_name = full_name[0]
            user.last_name = full_name[1] if len(full_name) > 1 else ''

   
            user.set_password(form.cleaned_data['password'])
            user.save()

      
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = form.cleaned_data['phone_number']
            profile.role = form.cleaned_data['role']
            profile.save()

            messages.success(request, "Account created successfully! Please log in.")

            return redirect('therapy_hub:login')
    else:
        form = SignUpForm()

    return render(request, 'therapy_hub/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            Profile.objects.get_or_create(user=user)

            return redirect('therapy_hub:dashboard')

        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "therapy_hub/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('therapy_hub:login')

@login_required(login_url='/therapy_hub/login/')
def dashboard(request):
        return render(request, "therapy_hub/dashboard.html")

@login_required(login_url='/therapy_hub/login/')
def client_dashboard(request):
    return render(request, 'therapy_hub/client_dashboard.html')

@login_required(login_url='/therapy_hub/login/')
def counsellor_dashboard(request):
    return render(request, 'therapy_hub/counsellor_dashboard.html')

from django.shortcuts import render

from django.db.models import Sum
@login_required(login_url='/therapy_hub/login/')
def earnings_report(request):
    detailed_earnings = Booking.objects.all().order_by('-date')

    total_earnings = detailed_earnings.filter(status='paid').aggregate(
        total=Sum('price')
    )['total'] or 0

    context = {
        'detailed_earnings': detailed_earnings,
        'total_earnings': total_earnings
    }

    return render(request, 'therapy_hub/earnings_report.html', context)
@login_required(login_url='/therapy_hub/login/')
def appointments(request):
    context = {
        "upcoming_appointments": []
    }
    return render(request, "therapy_hub/appointments.html", context)

@login_required(login_url='/therapy_hub/login/')
def profile(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.profile.phone = request.POST.get("phone")

        if 'avatar' in request.FILES:
            user.profile.avatar = request.FILES['avatar']

        password = request.POST.get("password")
        if password:
            user.set_password(password)

        user.save()
        user.profile.save()
        return redirect('therapy_hub:profile')

    return render(request, "therapy_hub/profile.html")

@login_required(login_url='/therapy_hub/login/')
def session_history(request):
    sessions = Session.objects.filter(client=request.user).order_by('-date')
    context = {"sessions": sessions}
    return render(request, "therapy_hub/session_history.html", context)

@login_required(login_url='/therapy_hub/login/')
def client_payments(request):
    payments = Payment.objects.filter(client=request.user).order_by('-paid_at')

    return render(request, "therapy_hub/client_payments.html", {
        "payments": payments
    })


def privacy_policy(request):
    return render(request, 'therapy_hub/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'therapy_hub/terms_conditions.html')

def our_story(request):
    return render(request, 'therapy_hub/our_story.html')