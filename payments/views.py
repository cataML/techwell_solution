import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import requests, uuid
from therapy_hub.models import Booking
from prodev.models import QuoteRequest
from digital.models import BookNow 
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def initialize_payment(request):
    if request.method == "POST":
        # Get current site config
        current_domain = request.get_host()
        config = settings.SITE_CONFIG.get(current_domain)
        if not config:
            return JsonResponse({'error': 'Unknown site'}, status=400)

        # Get email from user (logged-in or guest)
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST.get("email")
            if not email:
                return JsonResponse({'error': 'Email is required for guests'}, status=400)

        # Get amount
        try:
            amount = int(request.POST.get("amount")) * 100  # Paystack expects kobo
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        # Callback URL after payment
        callback_url = request.build_absolute_uri(config['callback_path'])

        # Paystack initialization request
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": email,
            "amount": amount,
            "callback_url": callback_url,
            "metadata": {
                "site_name": config['name'],
                "app": request.POST.get("app", "unknown"),  # optional
                "service_name": request.POST.get("service_name", "General Payment")
            }
            # Do NOT include "phone" here — Paystack will prompt user for phone
        }

        try:
            response = requests.post(
                settings.PAYSTACK_INITIALIZE_URL,
                json=data,
                headers=headers
            )
            res_data = response.json()
        except Exception as e:
            return JsonResponse({'error': f'Payment request failed: {str(e)}'}, status=500)

        if res_data.get("status"):
            # Redirect user to Paystack payment page (checkout modal)
            return redirect(res_data["data"]["authorization_url"])
        else:
            return JsonResponse({'error': res_data.get("message", "Payment initialization failed")}, status=400)

    # If GET request, render checkout form
    return render(request, "payments/checkout.html")



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

    # ------- SUCCESSFUL TRANSACTION --------
    if data.get('status') and data['data']['status'] == 'success':

        email = data['data']['customer']['email']
        amount = data['data']['amount'] // 100
        service_name = data['data']['metadata'].get('service_name', '').lower()
        app_name = data['data']['metadata'].get('app', '').lower()

        booking = None

        # 1️⃣ THERAPY HUB — Booking model
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

        # 2️⃣ PRODEV — QuoteRequest model
        elif app_name == "prodev":
            try:
                booking = QuoteRequest.objects.filter(
                    email=email,
                    plan__icontains=service_name  # use plan field
                ).latest('created_at')

                booking.status = "paid"
                booking.save()

                return render(request, "prodev/booking_success.html",
                              {"booking": booking})

            except QuoteRequest.DoesNotExist:
                return render(request, "prodev/payment_failed.html",
                              {"error": "Prodev booking not found."})

        # 3️⃣ DIGITAL — BookNow model
        elif app_name == "digital":
            try:
                booking = BookNow.objects.filter(
                    email=email,
                    service__icontains=service_name
                ).latest('created_at')

                booking.status = "paid"
                booking.save()

                return render(request, "digital/booking_success.html",
                              {"booking": booking})

            except BookNow.DoesNotExist:
                return render(request, "digital/payment_failed.html",
                              {"error": "Digital booking not found."})

        # Unknown app
        return HttpResponse("Unknown app in metadata.", status=400)

    # If transaction not successful
    return HttpResponse("Payment not successful.", status=400)

@csrf_exempt
def payment_callback(request):

    if request.method == "GET":
        reference = request.GET.get("reference")
        if not reference:
            return redirect("digital:client")
    
    # 2️⃣ Handle Paystack POST webhook
    elif request.method == "POST":
        try:
            payload = json.loads(request.body)
            reference = payload.get("reference")
        except Exception:
            return redirect("digital:client")
    else:
        return redirect("digital:client")

    # 3️⃣ Verify with Paystack
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"

    try:
        resp = requests.get(verify_url, headers=headers)
        data = resp.json()
    except Exception:
        return redirect("digital:client")

    # 4️⃣ SUCCESS
    if data.get("status") and data["data"]["status"] == "success":

        email = data["data"]["customer"]["email"]
        service_name = data["data"]["metadata"].get("service_name", "").lower()
        app_name = data["data"]["metadata"].get("app", "").lower()
        # 1️⃣ THERAPY HUB — Booking model
        if app_name == "therapy_hub":
            try:
                booking = Booking.objects.filter(
                    email=email,
                    session_type__icontains=service_name
                ).latest("created_at")

                booking.status = "paid"
                booking.save()

                return render(request, "therapy/payment_success.html",
                              {"booking": booking})

            except Booking.DoesNotExist:
                return render(request, "therapy/payment_failed.html",
                              {"error": "Therapy booking not found."})

        # 2️⃣ PRODEV — QuoteRequest model
        elif app_name == "prodev":
            try:
                booking = QuoteRequest.objects.filter(
                    email=email,
                    plan__icontains=service_name
                ).latest("created_at")

                booking.status = "paid"
                booking.save()

                return render(request, "prodev/booking_success.html",
                              {"booking": booking})
            except QuoteRequest.DoesNotExist:
                
                return redirect("prodev:dashboard")

        # 3️⃣ DIGITAL — BookNow model
        elif app_name == "digital":
            try:
                booking = BookNow.objects.filter(
                    email=email,
                    service__icontains=service_name
                ).latest("created_at")

                booking.status = "paid"
                booking.save()

                return render(request, "digital/booking_success.html",
                              {"booking": booking})

            except BookNow.DoesNotExist:
                return redirect("digital:index")

        # If app name does not match any known platform
        return HttpResponse("Unknown app in metadata.", status=400)

    # ---------------------------- FAILED PAYMENT ----------------------------
    return HttpResponse("Payment not successful.", status=400)



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
        print("PAYSTACK RESPONSE:", res_data)  

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


def checkout_prodev(request, pk):
    quote = get_object_or_404(QuoteRequest, pk=pk)

    plans = {
        "basic": {"name": "Basic Plan", "price": 50000},
        "standard": {"name": "Standard Plan", "price": 100000},
        "premium": {"name": "Premium Plan", "price": 150000},
    }

    selected_plan = plans.get(quote.plan)

    if not selected_plan:
        return JsonResponse({"error": "Invalid plan"}, status=400)

    if request.method == "POST":
        amount = selected_plan["price"] * 100   #
        email = quote.email                     
        service_name = selected_plan["name"]

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": email,
            "amount": amount,
            "metadata": {
                "service": service_name,
                "quote_id": quote.pk,
                "plan": quote.plan,
            },
            "callback_url": request.build_absolute_uri('/payments/verify/'),
        }

        response = requests.post(settings.PAYSTACK_INITIALIZE_URL, json=data, headers=headers)
        res_data = response.json()
        print("PAYSTACK RESPONSE:", res_data)

        if res_data.get("status"):
            return redirect(res_data["data"]["authorization_url"])

        return JsonResponse(res_data, status=400)

    return render(request, "payments/checkout_prodev.html", {
        "plan": selected_plan,
        "plan_key": quote.plan,
        "quote": quote,
    })


def checkout_digital(request, pk):
    book_now = get_object_or_404(BookNow, id=pk)

    service_key = (
        book_now.service.lower()
        .replace(" ", "_")
        .replace("/", "")
        .replace("__", "_")
        .strip()
    )

    conversion_map = {
        "tsc_services": "tsc",
        "sha_nssf_services": "sha_nssf",
        "data_entry": "data_entry",
        "pdf_conversion": "pdf_conversion",
        "computer_lessons": "computer_lessons",
        "typng": "typing", 
        "daily pass": "daily pass",
        "monthly subscription": "monthly subscription",
    }

    service_key = conversion_map.get(service_key, service_key)

    SERVICE_PRICES = {
        'government': 200,
        'tsc': 250,
        'sha_nssf': 300,
        'data_entry': 150,
        'typing': 1,
        'pdf_conversion': 100,
        'daily_pass': 300,
        'monthly subscription': 4500,
        'computer_lessons': 3000,
        'other': 100,
        
    }

    amount = SERVICE_PRICES.get(service_key, 0)

    context = {
        'booking': book_now,
        'amount': amount,
        'service_name': book_now.service,
        'source': 'digital',
    }

    return render(request, 'payments/checkout_digital.html', context)     
