def calculate_stats(records, field):
    if field not in ['duration', 'price']:
        return {'error': 'Invalid field'}

    values = [record[field] for record in records]
    return {
        'average': sum(values) / len(values),
        'max': max(values),
        'min': min(values)
    }
