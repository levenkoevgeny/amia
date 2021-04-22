from django.contrib import admin
from .models import *


@admin.register(DateForAppointment)
class DateForAppointmentPageAdmin(admin.ModelAdmin):
    list_display = ('date_appointment', 'month', 'day_of_week', 'day_of_week_number', 'day_of_month_number', 'is_holiday', 'is_sunday')
    list_filter = ('date_appointment', 'is_holiday',)
    search_fields = ['date_appointment', 'month']


@admin.register(Appointment)
class AppointmentPageAdmin(admin.ModelAdmin):
    list_display = ('date_appointment', 'time_interval', 'last_name', 'date_of_birth', 'date_of_write', 'is_booked', 'comment')
    list_filter = ('is_booked',)
    search_fields = ['last_name']
    list_editable = ('is_booked',)
