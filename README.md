В работе...
# Marketplace Data Pipeline

Проект по сбору и анализу данных о продажах маркетплейса. Включает скрипты для загрузки данных по API, хранения в PostgreSQL и аналитический дашборд в Metabase.

## Инфраструктура

Для выполнения проекта арендован VPS-сервер со следующими характеристиками:
- Операционная система: Ubuntu 22.04 / CentOS 8
- Панель управления: ISPmanager
- База данных: PostgreSQL
- Развёрнут Docker с контейнером Metabase

## Структура проекта

marketplace-data-pipeline/
├── src/                     # Исходный код
│   ├── api_client/          # Клиент для работы с API
│   ├── database/            # Подключение к БД и создание таблиц
│   └── pipelines/           # Скрипты загрузки данных
├── sql/                     # SQL-скрипты
│   └── init.sql             # Создание таблицы sales
├── notebooks/               # Jupyter ноутбуки с анализом
├── requirements.txt         # Зависимости Python
├── .env.example             # Пример файла с переменными окружения
└── README.md                # Этот файл

## Установка и запуск

### 1. Клонирование репозитория

git clone https://github.com/username/marketplace-data-pipeline.git
cd marketplace-data-pipeline

### 2. Настройка виртуального окружения

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

### 3. Настройка переменных окружения

Скопируйте .env.example в .env и заполните данными для подключения к БД.

### 4. Инициализация базы данных

psql -h localhost -U marketplace_user -d marketplace -f sql/init.sql

### 5. Запуск скриптов

python -m src.pipelines.historical_load
python -m src.pipelines.daily_load

### Логирование

Все действия скриптов записываются в файл `marketplace_load.log` в формате:

2026-04-24 12:10:58,556 - INFO - Сводка за 2026-04-23: получено 1577 записей, загружено 1577
2026-04-24 12:10:58,675 - INFO - Загрузка успешно завершена

Основные события:
- успешная загрузка данных за дату
- количество полученных и загруженных записей
- ошибки подключения к API или БД
- пропуск дублей (уникальное ограничение)

