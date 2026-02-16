from django.contrib import admin
from .models import ContactMessage, BookNow, Appointment, Task, Payment, Message, ClientProfile, Booking, ClientPayment, DigitalServices, DigitalBlog, DigitalTeam


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
@admin.action(description="Mark selected appointments as completed")
def mark_completed(modeladmin, request, queryset):
    queryset.update(status='completed')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    list_editable = ('status',)
    actions = [mark_completed]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'completed':
            return ('status',)
        return ()
admin.site.register(Task)
admin.site.register(Payment)
admin.site.register(Message)
admin.site.register(ClientProfile)
admin.site.register(Booking)


@admin.register(DigitalServices)
class DigitalServicesAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)

admin.site.register(DigitalBlog)

@admin.register(DigitalTeam)
class DigitalTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active')
    list_filter = ('is_active',)