from django.shortcuts import render
from django.conf import settings
from constants.params import MAX_TEMPERATURE

def index(request):
    context = {
        "WS_DATA_URL": settings.WS_DATA_URL,
        "MAX_TEMPERATURE": MAX_TEMPERATURE
    }
    return render(request, 'monitor.html', context)