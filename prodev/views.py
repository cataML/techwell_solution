from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm, SignUpForm, QuoteRequestForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import QuoteRequest, ProdevProfile, Project, Task, Message, Review, Projects, Invoice, Messages, Projectss, Tasks, MessageDev, ProjectOne, TaskOne, UserSettings
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def index(request):
    form = ContactForm()
    return render(request, 'prodev/index.html', {'form': form})
    
def contact(request):
    return render(request, 'prodev/contact.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prodev:success_contact')
        
    else:
        form = ContactForm()
    return render(request, 'prodev/contact.html', {'form':form})
def success_contact(request):
    return render(request, 'prodev/success_contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)


            full_name = form.cleaned_data['full_name'].split(' ', 1)
            user.first_name = full_name[0]
            user.last_name = full_name[1] if len(full_name) > 1 else ''

   
            user.set_password(form.cleaned_data['password1'])
            user.save()

      
            profile, created = ProdevProfile.objects.get_or_create(user=user)
            profile.phone_number = form.cleaned_data['phone_number']
            profile.role = form.cleaned_data['role']
            profile.save()

            messages.success(request, "Account created successfully! Please log in.")

            return redirect('prodev:login')
    else:
        form = SignUpForm()

    return render(request, 'prodev/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

      
            profile, created = ProdevProfile.objects.get_or_create(user=user)

    
            if profile.role == 'client':
                return redirect('prodev:client_dashboard')
            elif profile.role == 'developer':
                return redirect('prodev:developer_dashboard')

            return redirect('dashboard')  
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "prodev/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('prodev:login')

@login_required(login_url='/prodev/login/')
def request_quote(request):
    plan_key = request.GET.get("plan")  

    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('prodev:quote_success')
    else:
        form = QuoteRequestForm(initial={"plan": plan_key})

    return render(request, "prodev/request_quote.html", {
        "form": form,
        "plan_key": plan_key,
    })

@login_required(login_url='/prodev/login/')
def quote_success(request):
    return render(request, "prodev/quote_success.html", {"name": quote.full_name})

@login_required(login_url='/prodev/login/')
def dashboard(request):
    quotes = QuoteRequest.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'prodev/dashboard.html', {'quotes': quotes})


@login_required
def developer_dashboard(request):
    user = request.user
    total_projects = Project.objects.filter(assigned_to=user, status='ongoing').count()
    tasks_completed = Task.objects.filter(updated_by=user, status='completed').count()
    new_messages = Message.objects.filter(user=user, read=False).count()
    pending_reviews = Review.objects.filter(project__assigned_to=user, status='pending').count()
    recent_projects = Project.objects.filter(assigned_to=user).order_by('-created_at')[:5]

    context = {
        'total_projects': total_projects,
        'tasks_completed': tasks_completed,
        'new_messages': new_messages,
        'pending_reviews': pending_reviews,
        'recent_projects': recent_projects,
    }

    return render(request, 'prodev/developer_dashboard.html', context)


@login_required
def overview(request):
    total_projects = Projectss.objects.count()
    active_tasks = Tasks.objects.filter(completed=False).count()
    completed_tasks = Tasks.objects.filter(completed=True).count()
    team_members = sum(p.team_members for p in Project.objects.all())
    recent_projects = Projectss.objects.order_by('-deadline')[:5]

    context = {
        "total_projects": total_projects,
        "active_tasks": active_tasks,
        "completed_tasks": completed_tasks,
        "team_members": team_members,
        "recent_projects": recent_projects
    }
    return render(request, "prodev/overview.html", context)

def analytics(request):
    total_projects = ProjectOne.objects.count()
    active_tasks = TaskOne.objects.filter(completed=False).count()
    completed_tasks = TaskOne.objects.filter(completed=True).count()
    team_members = sum(p.team_members for p in ProjectOne.objects.all())

    today = timezone.now().date()
    tasks_over_time = []
    labels = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        completed_count = TaskOne.objects.filter(completed=True, date_completed=day).count()
        tasks_over_time.append(completed_count)
        labels.append(day.strftime("%a"))

    project_status_counts = ProjectOne.objects.values('status').annotate(count=Count('id'))

    status_labels = [p['status'] for p in project_status_counts]
    status_data = [p['count'] for p in project_status_counts]

    context = {
        "total_projects": total_projects,
        "active_tasks": active_tasks,
        "completed_tasks": completed_tasks,
        "team_members": team_members,
        "tasks_over_time": tasks_over_time,
        "tasks_labels": labels,
        "status_labels": status_labels,
        "status_data": status_data
    }

    return render(request, "prodev/analytics.html", context)
def dev_messages(request):
    messages = MessageDev.objects.order_by('-timestamp') 
    return render(request, "prodev/dev_messages.html", {"messages": messages})

@login_required
def settings_page(request):
    user = request.user
    settings, created = UserSettings.objects.get_or_create(user=user)

    if request.method == "POST":
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()

        settings.email_notifications = 'email_notifications' in request.POST
        settings.dark_mode = 'dark_mode' in request.POST
        settings.profile_visibility = request.POST.get('profile_visibility', 'public')

        if request.FILES.get('profile_picture'):
            settings.profile_picture = request.FILES['profile_picture']

        settings.save()

        messages.success(request, "Settings updated successfully!")
        return redirect('prodev:settings_page')

    return render(request, "prodev/settings_page.html", {"settings": settings, "user": user})


@login_required
def client_dashboard(request):
    user = request.user

    active_projects = Projects.objects.filter(client=user, status='ongoing').count()
    pending_payments = Invoice.objects.filter(client=user, paid=False).count()
    unread_messages = Messages.objects.filter(recipient=user, read=False).count()

    recent_projects = Projects.objects.filter(client=user).order_by('-updated_at')[:5]
    recent_messages = Messages.objects.filter(recipient=user).order_by('-created_at')[:5]
    recent_invoices = Invoice.objects.filter(client=user).order_by('-created_at')[:5]

    activity = []

    for p in recent_projects:
        activity.append({
            'type':'project',
            'text': f'Project "{p.title}" updated by {p.updated_by.username if p.updated_by else "N/A"}',
            'time': p.updated_at
        })

    for m in recent_messages:
        activity.append({'type':'message', 'text': f'New message from {m.sender.username}', 'time': m.created_at})

    for i in recent_invoices:
        if not i.paid:
            activity.append({'type':'invoice', 'text': f'Invoice #{i.id} awaiting payment', 'time': i.created_at})

    activity = sorted(activity, key=lambda x: x['time'], reverse=True)[:10]

    context = {
        'active_projects': active_projects,
        'pending_payments': pending_payments,
        'unread_messages': unread_messages,
        'activity': activity,
    }

    return render(request, 'prodev/client_dashboard.html', context)

@login_required
def client_messages(request):
    messages = Messages.objects.filter(recipient=request.user, read=False)
    return render(request, 'prodev/client_messages.html', {'messages': messages})

@login_required
def client_payments(request):
    invoices = Invoice.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'prodev/client_payments.html', {'invoices': invoices})