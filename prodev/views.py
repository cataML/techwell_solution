from django.shortcuts import render, redirect
from .forms import ContactForm, QuoteRequestForm
from .models import ProdevService, Project, BlogPost

# Create your views here.
def index(request):
    form = ContactForm()
    services = ProdevService.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True).order_by("-created_at")
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'prodev/index.html', {
        'form': form,
        'services': services,
        'projects': projects,
        'blogs': blogs
        })
    
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
    
def request_quote(request):
    plan_key = request.GET.get("plan")  
    form = QuoteRequestForm(initial={"plan": plan_key} if plan_key else None)

    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            
            # Ensure plan is set from POST data
            plan_selected = request.POST.get("plan")
            if not plan_selected:
                form.add_error('plan', 'Please select a valid plan.')
                return render(request, "prodev/request_quote.html", {"form": form, "plan_key": plan_key})
            
            quote.plan = plan_selected
            quote.save()
            return redirect('payments:checkout_prodev', pk=quote.pk)
    else:
        form = QuoteRequestForm(initial={"plan": plan_key} if plan_key else None)

    return render(request, "prodev/request_quote.html", {
        "form": form,
        "plan_key": plan_key,
    })


def quote_success(request):
    return render(request, "prodev/quote_success.html")

