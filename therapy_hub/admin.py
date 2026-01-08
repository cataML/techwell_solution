from django.contrib import admin
from .models import Contact, Booking, Payments, Profile, Session, TeamMember, TherapyService, CaseStudy, Event

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

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'is_active')
    list_filter = ('is_active',)


@admin.register(TherapyService)
class TherapyServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time')
    list_filter = ('date',)
    search_fields = ('title',)