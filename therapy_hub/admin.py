from django.contrib import admin
from .models import Contact, Booking, Payments, Profile, Session

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "date", "status")
    search_fields = ("name", "email", "service")
    list_filter = ("service", "status", "date")

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("client", "amount", "method", "paid_at")
    list_filter = ("method", "paid_at")
    search_fields = ("client__username",)

admin.site.register(Contact)

admin.site.register(Profile)

admin.site.register(Session)