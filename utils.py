def calculate_stats(records):
    # Получаем все цены из записей
    values = [record['price'] for record in records]

    # Проверяем, есть ли записи с ценами
    if not values:
        return {'error': 'Нет записей для расчета статистики.'}

    # Возвращаем среднее, минимальное и максимальное значение цен
    return {
        'average': sum(values) / len(values),
        'max': max(values),
        'min': min(values)
    }
