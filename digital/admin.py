from django.contrib import admin
from .models import ContactMessage, BookNow, Appointment, Task, Payment, Message, StaffMessage, ClientProfile, Booking, ClientPayment, ClientMessage


admin.register(BookNow)
class BookNowAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "contact", "service", "created_at")
    search_fields = ("name", "email", "service")
    list_filter = ("service", "created_at")

@admin.register(ClientPayment)
class ClientPaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "method", "status", "booking")
    list_filter = ("status", "method", "date")
    search_fields = ("user__username",)

admin.site.register(ContactMessage)
admin.site.register(Appointment)
admin.site.register(Task)
admin.site.register(Payment)
admin.site.register(Message)
admin.site.register(StaffMessage)
admin.site.register(ClientProfile)
admin.site.register(Booking)
admin.site.register(ClientMessage)
