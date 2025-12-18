from django.contrib import admin
from prodev.models import Contact, QuoteRequest

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "plan", "status", "created_at")
    list_filter = ("plan", "status")
    search_fields = ("full_name", "email", "project_details")

admin.site.register(Contact)
