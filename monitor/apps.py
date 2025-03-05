from django.apps import AppConfig

class MonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitor'

    # def ready(self):
    #     import display.server_message

    def ready(self):
        # Импортируем планировщик только после полной загрузки приложения
        import monitor.scheduler as scheduler
        scheduler.scheduler.start()
