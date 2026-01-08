from django.contrib import admin
from prodev.models import Contact, QuoteRequest, ProdevService, Project

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "plan", "status", "created_at")
    list_filter = ("plan", "status")
    search_fields = ("full_name", "email", "project_details")

admin.site.register(Contact)

@admin.register(ProdevService)
class ProdevServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
