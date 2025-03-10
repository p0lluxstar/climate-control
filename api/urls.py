from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.get_all_data, name='all_data'),
    path('month/', views.get_month_data, name='last_month_data'),
    path('week/', views.get_week_data, name='last_week_data'),
    path('day/', views.get_day_data, name='last_day_data'),
    path('hour/', views.get_hour_data, name='last_hour_data'),
    path('latest/', views.get_latest_data, name='latest_data'),
]
