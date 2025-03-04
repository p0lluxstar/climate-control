from django.apps import AppConfig
from .scheduler import scheduler

class DisplayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'display'

    # def ready(self):
    #     import display.server_message

    # def ready(self):
    #     # Запуск планировщика только один раз
    #     if not scheduler.running:
    #         scheduler.start()
    #         print("Планировщик запущен!")