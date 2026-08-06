# ProfSoft AI Microservice

Сервис асинхронного поиска по документации (RAG) на базе FastAPI, PostgreSQL, Qdrant и APScheduler.

## Технологический стек

- **FastAPI** — веб-фреймворк
- **PostgreSQL + SQLAlchemy + Alembic** — база данных и миграции
- **Qdrant** — векторная база данных
- **AsyncIOScheduler (APScheduler)** — фоновый асинхронный воркер
- **Poetry** — управление зависимостями

## Запуск проекта

### 1. Файл конфигурации

Скопируйте шаблон переменных окружения:

```bash
cp env.example .env
```

### 2. Запуск сервисов

```bash
docker compose up --build -d
```

Сервер доступен по адресу `http://localhost:8000`.

### 3. Загрузка тестовых данных

Для наполнения базы тестовыми документами вызовите скрипт:

```bash
python scripts/seed_data.py
```

## Примеры использования API

### Добавление документа

```bash
curl -X POST http://localhost:8000/documents/ \
  -H "Content-Type: application/json" \
  -d '{
    "source": "wiki://policy",
    "text": "Ежегодный оплачиваемый отпуск составляет 28 календарных дней."
  }'
```

### Поиск ответа по базе знаний (RAG)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Сколько дней составляет отпуск?"}'
```

### Список документов и статусов

```bash
curl http://localhost:8000/documents/
```

## Структура проекта

```text
.
├── app/
│   ├── api/            # Эндпоинты FastAPI (documents, ask, health)
│   ├── core/           # Настройки и конфигурация
│   ├── db/             # Подключение к PostgreSQL
│   ├── models/         # Модели SQLAlchemy и схемы Pydantic
│   ├── services/       # Логика RAG, чанкинг и эмбеддинги
│   ├── vector/         # Клиент Qdrant DB
│   └── workers/        # Асинхронный планировщик APScheduler
├── alembic/            # Миграции базы данных
├── scripts/            # Скрипты загрузки тестовых данных
├── docker-compose.yml  # Оркестрация контейнеров
└── pyproject.toml      # Зависимости Poetry
```

## Вспомогательные интерфейсы

- Панель Qdrant: `http://localhost:6333/dashboard`
