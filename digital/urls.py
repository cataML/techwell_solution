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
    path('staff/appointments/', views.staff_appointments, name='staff_appointments'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('no-permission/', views.no_permission_view, name='no_permission'), 
    path('appointments/<int:appointment_id>/complete/', views.complete_appointment, name='complete_appointment'),
    path("appointments/completed/", views.completed_appointments,name="staff_completed_appointments"),
    path("staff/tasks/<int:task_id>/done/", views.mark_task_done, name="mark_task_done"),
    path('staff/tasks/', views.staff_tasks_dashboard, name='staff_tasks'),
    path('staff/payments/', views.staff_payments, name='staff_payments'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('inbox/', views.inbox, name='inbox'),
    path('messages/', views.messages_view, name='messages'),
    path('client/messages/', views.client_messages, name='client_messages'),
    path('profile/update/', views.profile_view, name='update_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('client/payments/', views.client_payments, name='client_payments'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions"),
    path("our_story/", views.our_story, name="our_story"),
    path('settings/', views.settings_view, name='settings'),

]