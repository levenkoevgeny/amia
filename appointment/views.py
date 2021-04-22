from django.shortcuts import render
import calendar
from .models import DateForAppointment, Appointment
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.db import transaction
from datetime import date
from .forms import AppointmentForm, DateForAppointmentForm
from .filters import AppointmentFilter, DateForAppointmentFilter
from django.core.paginator import Paginator


def index(request):
    return render(request, 'appointment/index.html')


@transaction.atomic
def get_dates(request):
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    time_intervals = []
    minute_intervals = ['00', '20', '40']

    for i in range(9, 19):
        time_intervals.append(str(i) + '.' + minute_intervals[0])
        time_intervals.append(str(i) + '.' + minute_intervals[1])
        time_intervals.append(str(i) + '.' + minute_intervals[2])

    cal = calendar.Calendar()

    DateForAppointment.objects.all().delete()

    for day in cal.itermonthdates(2021, 5):
        date_app = DateForAppointment(date_appointment=day,
                                      month=5,
                                      day_of_week=days[day.weekday()],
                                      day_of_week_number=day.weekday(),
                                      is_holiday=False)
        date_app.save()

        if date_app.day_of_week_number == 6:
            date_app.is_sunday = True
            date_app.is_holiday = True
        if date_app.day_of_week_number == 5:
            date_app.is_holiday = True
        if date_app.date_appointment.month != 5:
            date_app.day_of_month_number = 0
        date_app.save()

        for time_inter in time_intervals:
            appointment = Appointment(
                date_appointment=date_app,
                time_interval=time_inter,
                is_booked=False
            )
            appointment.save()

    for day in cal.itermonthdates(2021, 6):
        date_app = DateForAppointment(date_appointment=day,
                                      month=6,
                                      day_of_week=days[day.weekday()],
                                      day_of_week_number=day.weekday(),
                                      is_holiday=False)
        date_app.save()
        if date_app.date_appointment.day > 1:
            date_app.day_of_month_number = 0
        if date_app.day_of_week_number == 6:
            date_app.is_sunday = True
            date_app.is_holiday = True
        if date_app.day_of_week_number == 5:
            date_app.is_holiday = True
        if date_app.date_appointment.month != 6:
            date_app.day_of_month_number = 0
        date_app.save()

        for time_inter in time_intervals:
            appointment = Appointment(
                date_appointment=date_app,
                time_interval=time_inter,
                is_booked=False
            )
            appointment.save()

    return HttpResponseRedirect(reverse('appointment:index'))


class AppointmentEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Appointment):
            return str(obj)
        return super().default(obj)


def get_free_intervals(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        picker_date_id = request.POST['pickerdateid']
        date_obj = get_object_or_404(DateForAppointment,pk=picker_date_id)
        interval_list = Appointment.objects.filter(date_appointment=date_obj).filter(is_booked=False)
        return JsonResponse(serialize('json', interval_list, use_natural_foreign_keys=True, cls=AppointmentEncoder), safe=False)


def add_appointment(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        date_appointment_id = request.POST['date_appointment']
        appointment_id = request.POST['appointment']

        if validate(date_appointment_id, appointment_id):
            date_appointment_obj = get_object_or_404(DateForAppointment, pk=date_appointment_id)
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            if appointment.is_booked:
                return render(request, 'appointment/index.html',
                              {'error_message': "Время уже занято!"})
            else:
                appointment.date_appointment = date_appointment_obj
                appointment.last_name = request.POST['last_name']
                appointment.date_of_birth = request.POST['date_of_birth']
                appointment.date_of_write = timezone.now()
                appointment.comment = request.POST['comment']
                appointment.is_booked = True
                appointment.save()
                return redirect('/' + str(appointment.id) + '/success/')
        else:
            return render(request, 'appointment/index.html', {'error_message': "Ошибка записи. Выберите дату и время!",
                                                              'last_name': request.POST['last_name'],
                                                              'comment': request.POST['comment'],
                                                              'date_of_birth': request.POST['date_of_birth']
                                                              })


def validate(date_appointment_id, appointment_id):
    check = False
    if date_appointment_id != '' and appointment_id != '':
        check = True
    return check


def success(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'appointment/success.html', {
        'last_name': appointment.last_name,
        'date_appointment': appointment.date_appointment.date_appointment,
        'time': appointment.time_interval,
    })


def dashboard(request):
    f = AppointmentFilter(request.GET, queryset=Appointment.objects.all())
    paginator = Paginator(f.qs, 200)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'appointment/dashboard/dashboard_main.html', {'list': items,
                                                                         'filter': f,
                                                                         })


def dashboard_dates(request):
    f = DateForAppointmentFilter(request.GET, queryset=DateForAppointment.objects.exclude(day_of_month_number=0))
    paginator = Paginator(f.qs, 200)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'appointment/dashboard/dashboard_dates.html', {'list': items,
                                                                         'filter': f,
                                                                         })


def appointment_update(request, appointment_id):
    if request.method == "POST":
        obj = get_object_or_404(Appointment, pk=appointment_id)
        form = AppointmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Ошибка редактирования!"
            return JsonResponse({'error': error_message}, safe=False)
    else:
        obj = get_object_or_404(Appointment, pk=appointment_id)
        form = AppointmentForm(instance=obj)
        return render(request, 'appointment/dashboard/appointment_update_form.html', {
            'form': form,
            'obj': obj,
        })


def date_for_appointment_update(request, date_for_appointment_id):
    if request.method == "POST":
        obj = get_object_or_404(DateForAppointment, pk=date_for_appointment_id)
        form = DateForAppointmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Ошибка редактирования!"
            return JsonResponse({'error': error_message}, safe=False)
    else:
        obj = get_object_or_404(DateForAppointment, pk=date_for_appointment_id)
        form = DateForAppointmentForm(instance=obj)
        return render(request, 'appointment/dashboard/date_for_appointment_update_form.html', {
            'form': form,
            'obj': obj,
        })

