from django.shortcuts import render, redirect
from .forms import ContactForm, QuoteRequestForm

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
    
def request_quote(request):
    plan_key = request.GET.get("plan", "basic")  

    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.plan = plan_key  
            quote.save()
            return redirect('payments:checkout_prodev', pk=quote.pk)
    else:
        form = QuoteRequestForm(initial={"plan": plan_key})

    return render(request, "prodev/request_quote.html", {
        "form": form,
        "plan_key": plan_key,
    })


def quote_success(request):
    return render(request, "prodev/quote_success.html")

