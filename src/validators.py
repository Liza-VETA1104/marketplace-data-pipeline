from datetime import datetime
from logging_setup import get_logger

logger = get_logger(__name__)

REQUIRED_FIELDS = {
    'client_id', 'gender', 'purchase_datetime', 'purchase_time_as_seconds_from_midnight',
    'product_id', 'quantity', 'price_per_item', 'discount_per_item', 'total_price'
}

def safe_int(value, field_name: str):
    try:
        return int(float(str(value).strip()))
    except (ValueError, TypeError):
        logger.warning("Не удалось преобразовать %s: %s", field_name, value)
        return None

def safe_float(value, field_name: str):
    try:
        return float(str(value).strip().replace(',', '.'))
    except (ValueError, TypeError):
        logger.warning("Не удалось преобразовать %s: %s", field_name, value)
        return None

def validate_record(record):
    if not isinstance(record, dict):
        return None
    
    # Проверка обязательных полей
    missing = REQUIRED_FIELDS - set(record.keys())
    if missing:
        logger.warning("Отсутствуют поля: %s", missing)
        return None
    
    # Проверка даты
    try:
        purchase_date = datetime.strptime(record['purchase_datetime'], '%Y-%m-%d').date()
    except (TypeError, ValueError):
        logger.warning("Неверный формат даты: %s", record.get('purchase_datetime'))
        return None
    
    # Пол — мягкая проверка (не блокируем)
    gender = record.get('gender', '').upper()
    if gender not in ('M', 'F'):
        logger.warning("Неизвестный пол: %s", gender)
    
    # Безопасное преобразование чисел
    client_id = safe_int(record['client_id'], 'client_id')
    time_seconds = safe_int(record['purchase_time_as_seconds_from_midnight'], 'purchase_time_seconds')
    product_id = safe_int(record['product_id'], 'product_id')
    quantity = safe_int(record['quantity'], 'quantity')
    
    if any(v is None for v in [client_id, time_seconds, product_id, quantity]):
        return None
    if quantity < 0:
        logger.warning("Отрицательное quantity: %s", quantity)
        return None
    
    price = safe_float(record['price_per_item'], 'price_per_item')
    discount = safe_float(record['discount_per_item'], 'discount_per_item')
    total = safe_float(record['total_price'], 'total_price')
    
    if any(v is None for v in [price, total]):
        return None
    
    return {
        'client_id': client_id,
        'gender': gender,
        'purchase_date': purchase_date,
        'purchase_time_seconds': time_seconds,
        'product_id': product_id,
        'quantity': quantity,
        'price_per_item': price,
        'discount_per_item': discount,
        'total_price': total
    }