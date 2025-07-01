from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'vaccine', 'signup_date', 'vaccination_date', 'time')
    list_filter = ('vaccination_date','user')
    search_fields = ('user', 'vaccine')