import os

# Определяем окружение
ENV = os.getenv("ENV", "local")

if ENV not in ("local", "dev", "prod"):
    raise ValueError("Invalid ENV value")

# Для локальной разработки загружаем .env
if ENV == "local":
    from dotenv import load_dotenv
    load_dotenv()

# База данных
DB_PARAMS = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# API
API_URL = os.getenv("API_URL")
if not API_URL:
    raise ValueError("API_URL is not set")
TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 5

# Логи
LOG_FILE = os.getenv("LOG_FILE", "marketplace_load.log")