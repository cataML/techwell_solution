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
    list_display = ('name', 'email', 'service', 'status', 'submitted_at')
    list_filter = ('service', 'status', 'submitted_at')
    search_fields = ('name', 'email', 'details')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)