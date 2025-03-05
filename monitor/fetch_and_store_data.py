import time
import threading
import requests
from .models import ClimateData


def fetch_and_store_data():
    while True:
        try:
            response = requests.get("http://127.0.0.1:5000/data", timeout=5)
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
            else:
                print("Некорректные данные, не удалось сохранить в базу.")
        except requests.RequestException as e:
            print(f"Ошибка при получении данных: {e}")

        time.sleep(30)  # Пауза в 10 секунд

# Запускаем функцию в отдельном потоке


def start_server_message_thread():
    server_thread = threading.Thread(target=fetch_and_store_data)
    server_thread.daemon = True  # Поток будет завершен при завершении основного процесса
    server_thread.start()


# Запуск
if __name__ == "__main__":
    start_server_message_thread()

    # Ваш код для запуска сервера Django
    # Например, запускаем сервер
    from django.core.management import execute_from_command_line
    import sys
    execute_from_command_line(sys.argv)
