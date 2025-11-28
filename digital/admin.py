from django.contrib import admin
from .models import ContactMessage, BookNow, Appointment, Task, Payment, Message                     
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at",)


@admin.register(BookNow)
class BookNowAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "contact", "service", "notes", "created_at")
    search_fields = ("name", "email", "service")

admin.site.register(Appointment)
admin.site.register(Task)
admin.site.register(Payment)
admin.site.register(Message)