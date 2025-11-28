from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import requests
from therapy_hub.models import Booking
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required
def initialize_payment(request):
    if request.method == 'POST':
        current_domain = request.get_host() 
        config = settings.SITE_CONFIG.get(current_domain)

        if not config:
            return JsonResponse({'error': 'Unknown site'}, status=400)

        email = request.user.email

        try:
            amount = int(request.POST.get('amount')) * 100 
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        callback_url = request.build_absolute_uri(config['callback_path'])

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": email,
            "amount": amount,
            "callback_url": callback_url,
            "metadata": {
                "site_name": config['name']
            }
        }

        try:
            response = requests.post(settings.PAYSTACK_INITIALIZE_URL, json=data, headers=headers)
            res_data = response.json()
        except Exception as e:
            return JsonResponse({'error': f'Payment request failed: {str(e)}'}, status=500)

        if res_data.get('status'):
            return redirect(res_data['data']['authorization_url'])
        else:
            return JsonResponse({'error': res_data.get('message', 'Payment initialization failed')}, status=400)

    return render(request, 'payments/checkout.html')


@login_required
def verify_payment(request):
    reference = request.GET.get('trxref') or request.GET.get('reference')
    if not reference:
        return render(request, "payments/payment_failed.html",
                      {"error": "No transaction reference found."})

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"

    try:
        resp = requests.get(verify_url, headers=headers)
        data = resp.json()
    except Exception:
        return render(request, "payments/payment_failed.html",
                      {"error": "Verification failed."})

    # ✔ Transaction successful?
    if data.get('status') and data['data']['status'] == 'success':

        email = data['data']['customer']['email']
        amount = data['data']['amount'] // 100
        service_name = data['data']['metadata'].get('service_name', '').lower()
        app_name = data['data']['metadata'].get('app', '').lower()  

        booking = None

        # 1️⃣ THERAPY HUB (Booking model)
        if app_name == "therapy_hub":
            try:
                booking = Booking.objects.filter(
                    email=email,
                    session_type__icontains=service_name
                ).latest('created_at')

                booking.status = "paid"
                booking.save()

                return render(request, "therapy/payment_success.html",
                              {"booking": booking})

            except Booking.DoesNotExist:
                return render(request, "therapy/payment_failed.html",
                              {"error": "TherapyHub booking not found."})
            
@csrf_exempt
def payment_callback(request):
    """Universal Paystack webhook handler for TherapyHub, Digital, ProDev, etc."""
    
    if request.method != 'POST':
        return redirect('digital:client')

    # Load webhook payload
    try:
        payload = json.loads(request.body)
        reference = payload.get("reference")
        if not reference:
            return redirect('digital:client')
    except Exception:
        return redirect('digital:client')

    # Verify the payment with Paystack
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"

    try:
        resp = requests.get(verify_url, headers=headers)
        data = resp.json()
    except Exception:
        return redirect('digital:dashboard')

    # Payment was successful?
    if data.get("status") and data["data"]["status"] == "success":

        email = data["data"]["customer"]["email"]
        service_name = data["data"]["metadata"].get("service_name", "")
        app_name = data["data"]["metadata"].get("app", "").lower()  # 👈 Detect app

        # 2️⃣ THERAPY HUB — Booking model
        if app_name == "therapy_hub":
            try:
                booking = Booking.objects.filter(
                    email=email,
                    session_type__icontains=service_name
                ).latest("created_at")

                booking.status = "paid"
                booking.save()

                return render(request, "therapy/payment_success.html", {"booking": booking})

            except Booking.DoesNotExist:
                return render(request, "payments/payment_failed.html",
                              {"error": "Therapy booking not found."})

        return render(request, "payments/payment_failed.html",
                      {"error": "Unknown app in metadata."})

   
    return render(request, "payments/payment_failed.html",
                  {"error": "Payment not successful."})


def checkout(request):
    if request.method == "POST":
        print("DEBUG: PAYSTACK_SECRET_KEY =", settings.PAYSTACK_SECRET_KEY)
        email = request.POST.get("email")
        amount = int(request.POST.get("amount")) * 100
        service_name = request.POST.get("service_name", "General Payment")

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": amount,
            "metadata": {"service": service_name},
            "callback_url": request.build_absolute_uri('/payments/verify/'),
        }

        response = requests.post(settings.PAYSTACK_INITIALIZE_URL, json=data, headers=headers)
        res_data = response.json()
        print("PAYSTACK RESPONSE:", res_data)  # 👈 see details in console

        if res_data.get("status"):
            return redirect(res_data["data"]["authorization_url"])
        return JsonResponse(res_data, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def checkout_therapy(request, pk):
    booking = get_object_or_404(Booking, id=pk)

    service_key = (
    booking.service.lower()
    .replace(" ", "_")
    .replace("/", "")
    .replace("__", "_")
    .strip()
    )

    conversion_map = {
        "individual_therapy": "individual",
        "couples_therapy": "couples",
        "corporate_therapy": "corporate",
        "basic_plan": "basic",
        "standard_plan": "standard",
        "premium_plan": "premium",
    }
    
    service_key = conversion_map.get(service_key, service_key)


    SERVICE_PRICES = {
        'individual': 2000,
        'couples': 3500,
        'corporate': 2500,
    }

    SUBSCRIPTION_PRICES = {
        "basic": 7000,
        "standard": 10000,
        "premium": 15000,
    }

    ALL_PRICES = {**SERVICE_PRICES, **SUBSCRIPTION_PRICES}

    amount = ALL_PRICES.get(service_key, 0)
    
    context = {
        'booking': booking,
        'amount': amount,
        'service_name': booking.service,
        'source': 'therapy_hub',
    }
    
    return render(request, 'payments/checkout_therapy.html', context)

       
