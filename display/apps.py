from django.apps import AppConfig

class DisplayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'display'

    # def ready(self):
    #     import display.server_message

    def ready(self):
        # Импортируем планировщик только после полной загрузки приложения
        import display.scheduler as scheduler
        scheduler.scheduler.start()
