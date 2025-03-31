import os
from apscheduler.schedulers.background import BackgroundScheduler
from monitor.models import ClimateData
import requests
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
import sqlite3
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta

load_dotenv()

# Функция, которая будет выполняться по расписанию


def getDataSensor():
    # print('запись в бд')
    try:
        response = requests.get(os.getenv('WS_DATA_URL'), timeout=5)
        response.raise_for_status()

        data = response.json()
        # print(data)

        temperature = data.get('temperature')
        humidity = data.get('humidity')

        if temperature is not None and humidity is not None:
            ClimateData.objects.create(
                temperature=temperature,
                humidity=humidity
            )
            print("Данные успешно сохранены в базу данных.")

            # Отправка email, если температура выше 23°C
            if temperature > 23.0:
                send_mail(
                    subject="Warning! High Temperature Detected",
                    message=f"The temperature has risen above 23°C. Current temperature: {temperature}°C.",
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


def deleteDataDB():
    # Подключение к базе данных
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    # Получаем текущую дату и вычитаем 8 дней
    days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d %H:%M:%S')

    # Удаление записей старше 8 дней
    cursor.execute("""
        DELETE FROM monitor_climatedata 
        WHERE created_at < ?
    """, (days_ago,))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()
    print('Записи старше 8 дней удалены')


# Инициализация планировщика
scheduler = BackgroundScheduler()

# Добавление задачи в планировщик
scheduler.add_job(getDataSensor, 'interval', seconds=300)
scheduler.add_job(deleteDataDB, CronTrigger(hour=3, minute=0))
