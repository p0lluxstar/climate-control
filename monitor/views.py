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


def get_all_data(request):
    """ Возвращает все данные """
    all_data = ClimateData.objects.all()

    if all_data:
        data_list = [
            {
                "created_at": data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "temperature": data.temperature,
                "humidity": data.humidity
            }
            for data in all_data
        ]
    else:
        return JsonResponse({'error': 'Нет данных'}, status=404)

    return JsonResponse(data_list, safe=False)


def get_last_hour_data(request):
    """ Возвращает данные за последний час """
    one_hour_ago = now() - timedelta(hours=1)  # Определяем границу времени
    recent_data = ClimateData.objects.filter(
        created_at__gte=one_hour_ago)  # Фильтруем записи

    if not recent_data.exists():
        return JsonResponse({'error': 'Нет данных за последний час'}, status=404)

    data_list = [
        {
            "created_at": data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": data.temperature,
            "humidity": data.humidity
        }
        for data in recent_data
    ]

    return JsonResponse(data_list, safe=False)


def get_latest_data(request):
    """ Возвращает последние данные о температуре и влажности """
    latest_data = ClimateData.objects.last()

    if latest_data:
        data_list = [{
            'created_at': latest_data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': latest_data.temperature,
            'humidity': latest_data.humidity
        }]
    else:
        return JsonResponse({'error': 'Нет данных'}, status=404)

    return JsonResponse(data_list, safe=False)
