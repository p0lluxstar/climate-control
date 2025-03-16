import os
import random
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Создаем экземпляр приложения Flask
ws = Flask(__name__)

CORS(ws, origins=[os.getenv('FRONTEND_URL')])

# Определяем маршрут (route) для запросов


@ws.route('/data', methods=['GET'])
def get_data():

    temperature = round(random.uniform(20, 21), 1)

    humidity = round(random.uniform(50, 51), 1)

    data = {
        'temperature': temperature,
        'humidity': humidity
    }

    return jsonify(data)  # Возвращаем данные как JSON


# Запуск сервера
if __name__ == '__main__':
    ws.run(host="0.0.0.0", debug=True)
