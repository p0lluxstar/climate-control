from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/all/', views.get_all_data, name='all_data'),
    path('api/last-hour/', views.get_last_hour_data, name='last_hour_data'),
    path('api/latest/', views.get_latest_data, name='latest_data'),
]
