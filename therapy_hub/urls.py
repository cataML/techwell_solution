from django.urls import path
from . import views
from .views import contact_view

app_name = 'therapy_hub'

urlpatterns = [
    path('', contact_view, {"template_name": "therapy_hub/index.html"}, name='index'),
    path('about/', contact_view, {"template_name": "therapy_hub/about.html"}, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', contact_view, {"template_name": "therapy_hub/contact.html"}, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('case_study/', views.case_study, name='case_study'),
    path('events/', views.events, name='events'),
    path('courses/', views.courses, name='courses'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path("client/", views.client_payments, name="client_payments"),
    path('counsellor_dashboard/', views.counsellor_dashboard, name='counsellor_dashboard'),
    path('earnings-report/', views.earnings_report, name='earnings_report'),
    path("appointments/", views.appointments, name="appointments"),
    path("profile/", views.profile, name="profile"),
    path("sessions/history/", views.session_history, name="session_history"),
     path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions"),
    path("our_story/", views.our_story, name="our_story"),
  ]