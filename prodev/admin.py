from django.contrib import admin
from .models import Contact, QuoteRequest
@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "plan", "status", "created_at")
    list_filter = ("plan", "status", "created_at")
    search_fields = ("full_name", "email", "project_details")