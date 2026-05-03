# Marketplace Data Pipeline

Проект по сбору и анализу данных о продажах маркетплейса. Включает скрипты для загрузки данных по API, хранения в PostgreSQL и аналитический дашборд в Metabase.

## Инфраструктура

Для выполнения проекта арендован VPS-сервер со следующими характеристиками:
- Операционная система: Ubuntu 22.04 / CentOS 8
- Панель управления: ISPmanager
- База данных: PostgreSQL
- Развёрнут Docker с контейнером Metabase

## Структура проекта
```text
marketplace-data-pipeline/

├── src/                     # Исходный код
│ ├── api.py                 # Запросы к API + retry

│ ├── config.py              # Конфигурация (env vars)
│ ├── daily_load.py          # Ежедневная загрузка (cron)
│ ├── db.py                  # Подключение к БД
│ ├── historical_load.py     # Историческая загрузка
│ ├── loaders.py             # Массовая вставка в БД
│ ├── logging_setup.py       # Настройка логирования
│ └── validators.py          # Валидация и очистка данных
├── sql/
│ └── init.sql               # Создание таблицы sales
├── .env.example             # Пример переменных окружения
├── .gitignore
├── README.md
└── requirements.txt
```
## Установка и запуск

### 1. Клонирование репозитория

```git clone https://github.com/username/marketplace-data-pipeline.git
cd marketplace-data-pipeline
```

### 2. Настройка виртуального окружения
```
python -m venv venv
```
```
.\venv\Scripts\Activate.ps1
```
```
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Скопируйте .env.example в .env и заполните данными для подключения к БД.

### 4. Инициализация базы данных
```
psql -h localhost -U marketplace_user -d marketplace -f sql/init.sql
```
### 5. Запуск скриптов
```
python -m src.pipelines.historical_load
```
```
python -m src.pipelines.daily_load
```
### Логирование

Все действия скриптов записываются в файл `marketplace_load.log` в формате:

2026-04-24 14:05:24,860 - __main__ - INFO - daily_load.py:81 - ETL start | date=2026-04-23

2026-04-24 14:05:26,601 - api - INFO - api.py:36 - Успешно получено 2536 записей за 2026-04-23

2026-04-24 14:05:26,828 - db - INFO - db.py:24 - Успешное подключение к БД

2026-04-24 14:05:27,031 - loaders - INFO - loaders.py:61 - За 2026-04-23: передано 2536 записей (дубликаты проигнорированы БД)

2026-04-24 14:05:27,031 - db - INFO - db.py:44 - Соединение с БД закрыто

Основные события:
- успешная загрузка данных за дату
- количество полученных и загруженных записей
- ошибки подключения к API или БД
- пропуск дублей (уникальное ограничение)

  
## Дашборд для оперативного отслеживания основных метрик
[Marketplace Dashboard](http://171.22.134.117:3000/public/dashboard/25f50cde-03e1-47f7-a8f7-a537fda31735)

### Метрики на дашборде:

- Выручка, AOV, DAU, Кол-во активных пользователей за период, Кол-во заказов, Заказов на пользователя

- Динамика выручки и DAU по дням

- Топ‑10 товаров по выручке и количеству продаж

- Фильтры по дате, товару и полу

## Автоматизация

На сервере настроен cron для ежедневного запуска в 7 утра:
```
0 7 * * * /marketplace-deploy/marketplace-data-pipeline/venv/bin/python /marketplace-deploy/marketplace-data-pipeline/src/daily_load.py >> /var/log/daily_etl.log 2>&1
```
