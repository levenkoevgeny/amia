from django.forms import ModelForm
from .models import Appointment, DateForAppointment


class AppointmentForm(ModelForm):

    class Meta:
        model = Appointment
        fields = ['last_name', 'comment', 'is_booked']


class DateForAppointmentForm(ModelForm):

    class Meta:
        model = DateForAppointment
        fields = ['is_holiday']

