from datetime import timedelta
from django.http import JsonResponse
import requests
from django.shortcuts import render
from .models import ClimateData
import plotly.graph_objects as go
from django.utils.timezone import now


def index(request):
    # data_all = ClimateData.objects.all()

    # # Извлекаем данные
    # dates = [data.created_at for data in data_all]
    # temperatures = [data.temperature for data in data_all]
    # humidities = [data.humidity for data in data_all]

    # # Создаём единый график
    # fig = go.Figure()

    # # Линия температуры
    # fig.add_trace(go.Scatter(
    #     x=dates, y=temperatures, name='Температура (°C)', line=dict(color='blue')
    # ))

    # # Линия влажности
    # fig.add_trace(go.Scatter(
    #     x=dates, y=humidities, name='Влажность (%)', line=dict(color='red')
    # ))

    # # Настройка осей и заголовка
    # fig.update_layout(
    #     title='Температура и влажность',
    #     xaxis_title='Дата',
    #     yaxis_title='Значение',
    #     legend=dict(x=0, y=1)  # Расположение легенды
    # )

    # graph_html = fig.to_html(full_html=False, config={'displayModeBar': False})

    # context = {
    #     'data_all': data_all,
    #     'graph_html': graph_html,
    # }

    return render(request, 'monitor.html')

