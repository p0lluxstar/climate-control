from apscheduler.schedulers.background import BackgroundScheduler
from monitor.models import ClimateData
import requests

# Функция, которая будет выполняться по расписанию


def print_server_status():
    print('запись в бд')
    # try:
    #     response = requests.get("http://127.0.0.1:5000/data", timeout=5)
    #     response.raise_for_status()

    #     data = response.json()
    #     print(data)

    #     temperature = data.get('temperature')
    #     humidity = data.get('humidity')

    #     if temperature is not None and humidity is not None:
    #         ClimateData.objects.create(
    #             temperature=temperature,
    #             humidity=humidity
    #         )
    #         print("Данные успешно сохранены в базу данных.")
    #     else:
    #         print("Некорректные данные, не удалось сохранить в базу.")
    # except requests.RequestException as e:
    #     print(f"Ошибка при получении данных: {e}")


# Инициализация планировщика
scheduler = BackgroundScheduler()

# Добавление задачи в планировщик
scheduler.add_job(print_server_status, 'interval', seconds=500)
