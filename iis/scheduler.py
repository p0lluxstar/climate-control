# Инициализация Django
import setup_django

# Импорты после setup
from datetime import timedelta
import os
import time
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from monitor.models import ClimateData
from constants.params import MAX_TEMPERATURE, TIME_GET_DATA_SENSOR, TIME_CHECK_SENSOR, TIME_DELETE_DATA_DB, DELETE_DATA_DB_DAYS


def getDataSensor():
    # print('запись в бд')
    try:
        response = requests.get(os.getenv('WS_DATA_URL'), timeout=5)
        response.raise_for_status()
        data = response.json()

        temperature = data.get('temperature')
        humidity = data.get('humidity')

        print(temperature, humidity)

        if temperature is not None and humidity is not None:
            ClimateData.objects.create(
                temperature=temperature,
                humidity=humidity
            )
            print("Данные успешно сохранены в базу данных.")

        # Отправка email, если температура выше 23°C
            if temperature > MAX_TEMPERATURE:
                send_mail(
                    subject="Warning! High Temperature Detected",
                    message=f"The temperature has risen above {MAX_TEMPERATURE}°C. Current temperature: {temperature}°C.",
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


def checkSensor():
    try:
        response = requests.get(os.getenv('WS_DATA_URL'), timeout=5)
        response.raise_for_status()

    except requests.RequestException as e:
        send_mail(
            subject="The temperature sensor is unavailable",
            message=f"Check the condition of the temperature sensor.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            # Укажите email получателя
                    recipient_list=[os.getenv('EMAIL_RECIPIENT')],
                    fail_silently=False,
        )
        print(f"Ошибка при получении данных: {e}")


def deleteDataDB():
    try:
        cutoff_date = timezone.now() - timedelta(days=DELETE_DATA_DB_DAYS)
        deleted_count, _ = ClimateData.objects.filter(
            created_at__lt=cutoff_date
        ).delete()
        print(
            f'Удалено {deleted_count} записей старше {DELETE_DATA_DB_DAYS} дней')
    except Exception as e:
        print(f'Ошибка при удалении записей: {e}')


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(getDataSensor, 'interval', seconds=TIME_GET_DATA_SENSOR)
    scheduler.add_job(checkSensor, 'interval', seconds=TIME_CHECK_SENSOR)
    scheduler.add_job(deleteDataDB, CronTrigger(
        hour=TIME_DELETE_DATA_DB["hour"], minute=TIME_DELETE_DATA_DB["minute"]))
    scheduler.start()
    print("Планировщик запущен. Нажмите Ctrl+C для остановки.")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Планировщик остановлен")
