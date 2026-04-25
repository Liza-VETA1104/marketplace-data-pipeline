import time
import psycopg2
from contextlib import contextmanager
from psycopg2 import OperationalError

from config import DB_PARAMS
from logging_setup import get_logger

logger = get_logger(__name__)

# -----------------------------
# CONNECTION
# -----------------------------

def get_connection(retries: int = 3, delay: int = 2):
    """Создаёт соединение с БД с retry логикой"""
    
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(
                connect_timeout=5,
                **DB_PARAMS
            )
            logger.info("Успешное подключение к БД")
            return conn

        except OperationalError as e:
            logger.error(
                "Попытка %s/%s: ошибка подключения к БД: %s",
                attempt, retries, e
            )

            if attempt < retries:
                time.sleep(delay)
            else:
                raise RuntimeError("Не удалось подключиться к БД после всех попыток")


def close_connection(conn):
    """Безопасное закрытие соединения"""
    try:
        if conn and not conn.closed:
            conn.close()
            logger.info("Соединение с БД закрыто")
    except Exception as e:
        logger.warning("Ошибка при закрытии соединения: %s", e)


# -----------------------------
# CONTEXT MANAGER (РЕКОМЕНДУЕТСЯ)
# -----------------------------

@contextmanager
def db_connection():
    """
    Контекстный менеджер для работы с БД:
    автоматически открывает и закрывает соединение
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        close_connection(conn)