from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/latest/', views.get_latest_data, name='latest_data'),
    path('api/all/', views.get_all_data, name='all_data'),
]
