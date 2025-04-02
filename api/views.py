from django.shortcuts import render
from monitor.models import ClimateData
from django.http import JsonResponse
from datetime import timedelta
from django.utils.timezone import now


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
        return JsonResponse({'no_data': 'No data available'}, status=404)

    return JsonResponse(data_list, safe=False)


def get_month_data(request):
    """ Возвращает данные за последний месяц """
    one_month_ago = now() - timedelta(days=30)  # Определяем границу времени (30 дней назад)
    recent_data = ClimateData.objects.filter(
        created_at__gte=one_month_ago)  # Фильтруем записи за последний месяц

    if not recent_data.exists():
        return JsonResponse({'no_data': 'There is no data for the last month'}, status=404)

    data_list = [
        {
            "created_at": data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": data.temperature,
            "humidity": data.humidity
        }
        for data in recent_data
    ]

    return JsonResponse(data_list, safe=False)


def get_week_data(request):
    """ Возвращает данные за последнюю неделю """
    one_week_ago = now() - timedelta(weeks=1)  # Определяем границу времени (7 дней назад)
    recent_data = ClimateData.objects.filter(
        created_at__gte=one_week_ago)  # Фильтруем записи за последнюю неделю

    if not recent_data.exists():
        return JsonResponse({'no_data': 'No data available for the last week'}, status=404)

    data_list = [
        {
            "created_at": data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": data.temperature,
            "humidity": data.humidity
        }
        for data in recent_data
    ]

    return JsonResponse(data_list, safe=False)


def get_day_data(request):
    """ Возвращает данные за последний день """
    one_day_ago = now() - timedelta(days=1)  # Определяем границу времени (24 часа назад)
    recent_data = ClimateData.objects.filter(
        created_at__gte=one_day_ago)  # Фильтруем записи за последний день

    if not recent_data.exists():
        return JsonResponse({'no_data': 'There is no data for the last day'}, status=404)

    data_list = [
        {
            "created_at": data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": data.temperature,
            "humidity": data.humidity
        }
        for data in recent_data
    ]

    return JsonResponse(data_list, safe=False)


def get_hour_data(request):
    """ Возвращает данные за последний час """
    one_hour_ago = now() - timedelta(hours=1)  # Определяем границу времени
    recent_data = ClimateData.objects.filter(
        created_at__gte=one_hour_ago)  # Фильтруем записи

    if not recent_data.exists():
        return JsonResponse({'no_data': 'Нет данных за последний час'}, status=404)

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
        return JsonResponse({'no_data': 'Нет данных'}, status=404)

    return JsonResponse(data_list, safe=False)
