from apscheduler.schedulers.background import BackgroundScheduler

# Функция, которая будет выполняться по расписанию
def print_server_status():
    print("Сервер запущен!")

# Инициализация планировщика
scheduler = BackgroundScheduler()

# Добавление задачи в планировщик
scheduler.add_job(print_server_status, 'interval', seconds=10)