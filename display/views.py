import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import ClimateData


def index(request):
    data_all = ClimateData.objects.all()
    return render(request, 'display.html', {'data_all': data_all})
