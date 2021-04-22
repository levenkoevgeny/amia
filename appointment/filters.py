import django_filters
from .models import Appointment, DateForAppointment
from django import forms


class DateForAppointmentFilter(django_filters.FilterSet):
    date_appointment = django_filters.DateFilter(field_name='date_appointment',
                                                 widget=forms.DateInput(
                                                     attrs={
                                                         'type': 'date'
                                                     }))

    class Meta:
        model = DateForAppointment
        fields = ['date_appointment', 'is_holiday']


class AppointmentFilter(django_filters.FilterSet):
    date_appointment__date_appointment = django_filters.DateFilter(field_name='date_appointment__date_appointment',
                                                 widget=forms.DateInput(
                                                     attrs={
                                                         'type': 'date'
                                                     }))
    last_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Appointment
        fields = ['date_appointment__date_appointment', 'last_name', 'is_booked']