from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

# Данные мастеров и стрижек
masters = {
    'male': ['Иванов', 'Петров'],
    'female': ['Смирнова', 'Федорова']
}

haircuts = {
    'male': [
        {'name': 'Классическая мужская стрижка', 'price': 200.0},
        {'name': 'Фейд', 'price': 250.0},
        {'name': 'Базз кат', 'price': 150.0},
        {'name': 'Помпадур', 'price': 300.0},
        {'name': 'Топ кнот', 'price': 350.0}
    ],
    'female': [
        {'name': 'Каре', 'price': 400.0},
        {'name': 'Боб', 'price': 450.0},
        {'name': 'Пикси', 'price': 350.0},
        {'name': 'Шэг', 'price': 500.0},
        {'name': 'Французская стрижка', 'price': 550.0}
    ]
}

# Список для хранения записей
records = []

# Упрощенная функция для расчета статистики по ценам
def calculate_price_stats(records):
    prices = [record['price'] for record in records]

    # Проверяем, есть ли записи с ценами
    if not prices:
        return {'error': 'Нет записей для расчета статистики.'}

    # Возвращаем среднее, минимальное и максимальное значение цен
    return {
        'average': sum(prices) / len(prices),
        'max': max(prices),
        'min': min(prices)
    }

@app.route('/')
def index():
    return render_template('index.html')  # Возвращаем HTML-страницу

@app.route('/data')
def get_data():
    response_data = {
        'message': 'Welcome to the haircut API',
        'masters': masters,
        'haircuts': haircuts
    }
    return jsonify(response_data), 200

@app.route('/records', methods=['POST'])
def manage_records():
    client_name = request.json.get('first_name')
    client_surname = request.json.get('last_name')
    master = request.json.get('master')
    haircut = request.json.get('haircut')
    date = request.json.get('date')

    if not client_name or not client_surname or not master or not haircut or not date:
        return jsonify({'error': 'Все поля должны быть заполнены.'}), 400

    selected_haircut = next((h for category in haircuts.values() for h in category if h['name'] == haircut), None)
    price = selected_haircut['price']

    new_record = {
        'id': len(records) + 1,
        'first_name': client_name,
        'last_name': client_surname,
        'master': master,
        'haircut': haircut,
        'date': datetime.strptime(date, '%Y-%m-%d').date(),
        'price': price
    }
    records.append(new_record)
    return jsonify(new_record), 201

@app.route('/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    for record in records:
        if record['id'] == record_id:
            return jsonify(record), 200
    return jsonify({'message': 'Запись не найдена'}), 404

@app.route('/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    updated_data = request.json
    for rec in records:
        if rec['id'] == record_id:
            rec['first_name'] = updated_data.get('first_name', rec['first_name'])
            rec['last_name'] = updated_data.get('last_name', rec['last_name'])
            rec['master'] = updated_data.get('master', rec['master'])
            rec['haircut'] = updated_data.get('haircut', rec['haircut'])
            rec['date'] = datetime.strptime(updated_data.get('date', rec['date'].isoformat()), '%Y-%m-%d').date()
            rec['price'] = next((h['price'] for category in haircuts.values() for h in category if h['name'] == rec['haircut']), rec['price'])
            return jsonify(rec), 200
    return jsonify({'message': 'Запись не найдена'}), 404

@app.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    global records
    records = [rec for rec in records if rec['id'] != record_id]
    return jsonify({'message': 'Запись удалена'}), 204

@app.route('/records/sort', methods=['GET'])
def sort_records():
    field = request.args.get('field')
    order = request.args.get('order', 'asc')

    if field not in ['first_name', 'last_name', 'master', 'date', 'price']:
        return jsonify({'error': 'Недопустимое поле для сортировки'}), 400

    sorted_records = sorted(records, key=lambda x: x[field], reverse=(order == 'desc'))
    return jsonify(sorted_records)

# Добавление маршрута для получения статистики по ценам
@app.route('/records/stats', methods=['GET'])
def get_price_stats():
    stats = calculate_price_stats(records)
    return jsonify(stats), 200 if 'error' not in stats else 400

if __name__ == '__main__':
    app.run(debug=True)
