# ProfSoft AI Microservice

Сервис асинхронного поиска по документации (RAG) на базе FastAPI, PostgreSQL, Qdrant и APScheduler.

## Технологический стек

- **FastAPI** — веб-фреймворк для обработки HTTP-запросов
- **PostgreSQL + SQLAlchemy + Alembic** — хранение метаданных документов и миграции
- **Qdrant** — векторная база данных
- **AsyncIOScheduler (APScheduler)** — фоновый асинхронный воркер для индексации
- **Poetry** — управление зависимостями и окружением

## Запуск проекта

### 1. Конфигурация перемененных окружения

Скопируйте шаблон файла конфигурации:

```bash
cp env.example .env
```

По умолчанию в `.env` включен автономный режим `TEST_MODE=True`, не требующий сторонних API-ключей. Для работы с внешними моделями укажите `GEMINI_API_KEY` или `OPENAI_API_KEY` и переключите `TEST_MODE=False`.

### 2. Запуск сервисов

```bash
docker compose up --build -d
```

Сервер FastAPI доступен по адресу `http://localhost:8000`.

### 3. Загрузка тестовых данных

Для наполнения базы тестовыми документами вызовите скрипт:

```bash
python scripts/seed_data.py
```

## Примеры использования API

### 1. Добавление документа

```bash
curl -X POST http://localhost:8000/documents/ \
  -H "Content-Type: application/json" \
  -d '{
    "source": "wiki://policy",
    "text": "Ежегодный оплачиваемый отпуск составляет 28 календарных дней."
  }'
```

### 2. Поиск ответа по базе знаний (RAG)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Сколько дней составляет отпуск?"}'
```

### 3. Получение списка документов и статусов

```bash
curl http://localhost:8000/documents/
```

## Веб-интерфейсы

- Панель управления Qdrant: `http://localhost:6333/dashboard`
