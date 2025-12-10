from django.contrib import admin
from therapy_hub.models import (
    Contact as TherapyContact,
    Booking as TherapyBooking,
    Profile as TherapyProfile,
    Session,
    Payment as TherapyPayment
)

# -----------------------------
# DIGITAL MODELS
# -----------------------------
from digital.models import (
    Contact as DigitalContact,
    BookNow as DigitalBookNow,
    Appointment,
    Task,
    Payment as DigitalPayment,
    Message,
    StaffMessage,
    ClientProfile,
    Booking as WorkstationBooking,
    ClientPayment,
    ClientMessage
)

# -----------------------------
# PRODEV MODELS
# -----------------------------
from prodev.models import Contact as ProdevContact, QuoteRequest

# -----------------------------
# THERAPY_HUB ADMIN
# -----------------------------
@admin.register(TherapyBooking)
class TherapyBookingAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "date", "status")
    search_fields = ("name", "email", "service")
    list_filter = ("service", "status", "date")

@admin.register(TherapyPayment)
class TherapyPaymentAdmin(admin.ModelAdmin):
    list_display = ("client", "amount", "method", "paid_at")
    list_filter = ("method", "paid_at")
    search_fields = ("client__username",)

# Other therapy models (simple registration)
admin.site.register(TherapyContact)
admin.site.register(TherapyProfile)
admin.site.register(Session)

# -----------------------------
# DIGITAL ADMIN
# -----------------------------
@admin.register(DigitalBookNow)
class DigitalBookNowAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "contact", "service", "created_at")
    search_fields = ("name", "email", "service")
    list_filter = ("service", "created_at")

@admin.register(ClientPayment)
class ClientPaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "method", "status", "booking")
    list_filter = ("status", "method", "date")
    search_fields = ("user__username",)

# Other digital models (simple registration)
admin.site.register(DigitalContact)
admin.site.register(Appointment)
admin.site.register(Task)
admin.site.register(DigitalPayment)
admin.site.register(Message)
admin.site.register(StaffMessage)
admin.site.register(ClientProfile)
admin.site.register(WorkstationBooking)
admin.site.register(ClientMessage)

# -----------------------------
# PRODEV ADMIN
# -----------------------------
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "plan", "status", "created_at")
    list_filter = ("plan", "status")
    search_fields = ("full_name", "email", "project_details")

# Other prodev models (simple registration)
admin.site.register(ProdevContact)

# -----------------------------
# ADMIN SITE CUSTOMIZATION
# -----------------------------
admin.site.site_header = "Techwell Unified Admin"
admin.site.site_title = "Techwell Admin"
admin.site.index_title = "Welcome to Techwell Unified Dashboard"