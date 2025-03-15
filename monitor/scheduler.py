import os
from apscheduler.schedulers.background import BackgroundScheduler
from monitor.models import ClimateData
import requests
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

# Функция, которая будет выполняться по расписанию


def getDataSensor():
    # print('запись в бд')
    try:
        response = requests.get(os.getenv('WS_DATA_URL'), timeout=5)
        response.raise_for_status()

        data = response.json()
        print(data)

        temperature = data.get('temperature')
        humidity = data.get('humidity')

        if temperature is not None and humidity is not None:
            ClimateData.objects.create(
                temperature=temperature,
                humidity=humidity
            )
            print("Данные успешно сохранены в базу данных.")

            # Отправка email, если температура выше 30°C
            if temperature > 20.8:
                send_mail(
                    subject="Warning! High Temperature Detected",
                    message=f"The temperature has risen above 30°C. Current temperature: {temperature}°C.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    # Укажите email получателя
                    recipient_list=[os.getenv('EMAIL_RECIPIENT')],
                    fail_silently=False,
                )
                print("Уведомление на email отправлено.")
        else:
            print("Некорректные данные, не удалось сохранить в базу.")
    except requests.RequestException as e:
        print(f"Ошибка при получении данных: {e}")


# Инициализация планировщика
scheduler = BackgroundScheduler()

# Добавление задачи в планировщик
scheduler.add_job(getDataSensor, 'interval', seconds=300)
