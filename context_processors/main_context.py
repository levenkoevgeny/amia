from appointment.models import DateForAppointment, Appointment


def counts(request):
    return {'date_list_may': DateForAppointment.objects.filter(month=5).order_by('date_appointment'),
            'date_list_june': DateForAppointment.objects.filter(month=6).order_by('date_appointment')[:7],
            }
