from django.urls import path
from . import views

app_name = 'digital'

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('service/', views.service, name='service'),
    path('blog', views.blog, name='blog'),
    path('contact_us/', views.Contact_us, name='contact_us'),
    path("success_contact/", views.success_contact, name="success_contact"),
    path("book_now/", views.book_now, name="book_now"),
    #path("booking-success/", views.booking_success, name="booking_success"),
    path('sign_up/', views.signup_view, name='sign_up'),
    path('log_in/', views.login_view, name='log_in'),
    path('client/', views.client, name='client'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.log_out, name='logout'),
    path("confirm_booking/<int:pk>/", views.confirm_booking, name="confirm_booking"),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('no-permission/', views.no_permission_view, name='no_permission'), 
    path('staff/appointments/', views.staff_appointments, name='staff_appointments'),
    path('staff/tasks/', views.staff_tasks, name='staff_tasks'),
    path('staff/payments/', views.staff_payments, name='staff_payments'),
    path('staff/messages/', views.staff_messages, name='staff_messages'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions"),
    path("our_story/", views.our_story, name="our_story"),

]