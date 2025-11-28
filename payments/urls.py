from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('verify/', views.verify_payment, name='verify'),
    path('initialize/', views.initialize_payment, name='initialize_payment'),
    path("callback/", views.payment_callback, name="payment_callback"),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/therapy_hub/<int:pk>/', views.checkout_therapy, name='checkout_therapy'),
    path('checkout/prodev/<int:pk>/', views.checkout_prodev, name='checkout_prodev'),
    path('checkout/digital/<int:pk>/', views.checkout_digital, name='checkout_digital'),
]