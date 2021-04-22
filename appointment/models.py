from django.db import models


class DateForAppointment(models.Model):
    date_appointment = models.DateField(verbose_name="Дата записи")
    month = models.IntegerField(verbose_name="Номер месяца", default=0)
    day_of_week = models.CharField(max_length=20, verbose_name="День недели", null=True, blank=True)
    day_of_week_number = models.IntegerField(verbose_name="Номер дня недели", null=True, blank=True)
    day_of_month_number = models.IntegerField(verbose_name="Номер дня месяца", null=True, blank=True)
    is_holiday = models.BooleanField(verbose_name="Выходной")
    is_sunday = models.BooleanField(verbose_name="Воскресенье", default=False)

    def __str__(self):
        return str(self.date_appointment)

    class Meta:
        ordering = ('date_appointment',)
        verbose_name = 'День записи'
        verbose_name_plural = 'Дни записи'


class Appointment(models.Model):
    date_appointment = models.ForeignKey(DateForAppointment, on_delete=models.CASCADE, verbose_name="Дата записи")
    time_interval = models.CharField(max_length=100, verbose_name="Временной интервал")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия", blank=True, null=True)
    date_of_birth = models.CharField(max_length=20, verbose_name="Дата рождения", blank=True, null=True)
    date_of_write = models.DateTimeField(verbose_name="Дата записи", blank=True, null=True)
    is_booked = models.BooleanField(verbose_name="Забронировано")
    comment = models.TextField(verbose_name="Комментарий к записи", blank=True, null=True)

    def __str__(self):
        return str(self.date_appointment.date_appointment) + ' ' + str(self.time_interval) + ' ' + str(self.last_name)

    class Meta:
        ordering = ('-date_appointment',)
        verbose_name = 'Запись на тестирование'
        verbose_name_plural = 'Записи на тестирование'