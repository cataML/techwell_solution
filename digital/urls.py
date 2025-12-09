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
    path('guest/<int:pk>/', views.choose_login_or_guest, name='guest'),
    path('sign_up/', views.signup_view, name='sign_up'),
    path('log_in/', views.login_view, name='log_in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('client/', views.client, name='client'),
    path('logout/', views.log_out, name='logout'),
    path("confirm_booking/<int:pk>/", views.confirm_booking, name="confirm_booking"),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('no-permission/', views.no_permission_view, name='no_permission'), 
    path('staff/appointments/', views.staff_appointments, name='staff_appointments'),
    path('staff/tasks/', views.staff_tasks, name='staff_tasks'),
    path('staff/payments/', views.staff_payments, name='staff_payments'),
    path('staff/messages/', views.staff_messages, name='staff_messages'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('payments/', views.payments, name='payments'),
    path('messages/', views.messages, name='messages'),
    #path("profile/", views.profile, name="profile"),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions"),
    path("our_story/", views.our_story, name="our_story"),

]