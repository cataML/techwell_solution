from django.urls import path
from . import views

app_name = 'prodev'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('success_contact/', views.success_contact, name='success_contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('request-quote/', views.request_quote, name='request_quote'),
    path('quote_success/', views.quote_success, name='quote_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("developer/dashboard/", views.developer_dashboard, name="developer_dashboard"),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path("client/messages/", views.client_messages, name="client_messages"),
    path("client/payments/", views.client_payments, name="client_payments"),
    path("overview/", views.overview, name="overview"),
    path("dev_messages/", views.dev_messages, name="dev_messages"),
    path("analytics/", views.analytics, name="analytics"),
    path("settings_page/", views.settings_page, name="settings_page"),
]
