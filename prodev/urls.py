from django.urls import path
from . import views

app_name = 'prodev'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('success_contact/', views.success_contact, name='success_contact'),
    path('request-quote/', views.request_quote, name='request_quote'),
    path('quote_success/', views.quote_success, name='quote_success'),
]
