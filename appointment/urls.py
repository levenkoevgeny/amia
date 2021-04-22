from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'appointment'

urlpatterns = [
    path('', views.index, name='index'),
    path('dates/', views.get_dates, name='get_dates'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('<appointment_id>/success/', views.success, name='success'),
    path('getfreeintervals', views.get_free_intervals, name='get_free_intervals'),
    path('dashboard/', login_required(views.dashboard), name='dashboard_main'),
    path('dashboard-dates/', login_required(views.dashboard_dates), name='dashboard_dates'),
    path('dashboard/appointment/<appointment_id>/update', views.appointment_update, name='appointment_update'),
    path('dashboard/date-for-appointment/<date_for_appointment_id>/update', views.date_for_appointment_update, name='date_for_appointment_update'),

]