import time
import requests

from config import API_URL, TIMEOUT, MAX_RETRIES, RETRY_DELAY
from logging_setup import get_logger

logger = get_logger(__name__)


def fetch_data_with_retry(date: str):
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(
                API_URL,
                params={"date": date},
                timeout=TIMEOUT
            )

            if not resp.ok:
                logger.warning(
                    "HTTP ошибка %s (попытка %d/%d)",
                    resp.status_code, attempt + 1, MAX_RETRIES
                )
                continue

            try:
                data = resp.json()
            except ValueError:
                logger.error("API вернул невалидный JSON")
                return None

            if not isinstance(data, list):
                logger.error("API вернул не список")
                return None

            logger.info("Успешно получено %d записей за %s", len(data), date)
            return data

        except requests.exceptions.Timeout:
            logger.warning("Таймаут (попытка %d/%d)", attempt + 1, MAX_RETRIES)
        except requests.exceptions.ConnectionError:
            logger.warning("Ошибка соединения (попытка %d/%d)", attempt + 1, MAX_RETRIES)
        except requests.exceptions.RequestException as e:
            logger.warning("Ошибка запроса: %s", e)

        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY * (2 ** attempt))  # exponential backoff

    logger.error("Не удалось получить данные за %s после %d попыток", date, MAX_RETRIES)
    return None