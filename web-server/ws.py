import random
from flask import Flask, jsonify
from flask_cors import CORS 

# Создаем экземпляр приложения Flask
ws = Flask(__name__)

CORS(ws, origins=["http://127.0.0.1:8000"])

# Определяем маршрут (route) для запросов
@ws.route('/data', methods=['GET'])
def get_data():

    temperature = round(random.uniform(30, 35), 1)

    humidity = round(random.uniform(60, 70), 1)

    data = {
        'temperature': temperature,
        'humidity': humidity
    }

    return jsonify(data)  # Возвращаем данные как JSON


# Запуск сервера
if __name__ == '__main__':
    ws.run(debug=True)