import os
import sys
import time
import django
from pathlib import Path
from django.conf import settings

# 1. Добавляем корень проекта в PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# 2. Устанавливаем переменную окружения ДО импорта моделей
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# 3. Инициализируем Django
django.setup()

# 4. Только теперь импортируем модели и другие зависимости
from monitor.models import ClimateData
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from apscheduler.triggers.cron import CronTrigger


def getDataSensor():
    #print('запись в бд')
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
            if temperature > 23:
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
    try:
        cutoff_date = timezone.now() - timedelta(days=8)
        deleted_count, _ = ClimateData.objects.filter(
            created_at__lt=cutoff_date
        ).delete()
        print(f'Удалено {deleted_count} записей старше 8 дней')
    except Exception as e:
        print(f'Ошибка при удалении записей: {e}')

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(getDataSensor, 'interval', seconds=300)
    scheduler.add_job(deleteDataDB, trigger=CronTrigger(hour=3, minute=10)),  # 03:00:00
    scheduler.start()
    print("Планировщик запущен. Нажмите Ctrl+C для остановки.")
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Планировщик остановлен")