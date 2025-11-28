from django.contrib import admin
from .models import Contact, Booking

# Register your models here.
@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)


@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'date', 'time', 'session', 'notes')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'service', 'date', 'time', 'session', 'notes')
    ordering = ('-created_at',)


