# AI Microservice

REST API-сервис для асинхронной обработки задач на базе FastAPI и PostgreSQL.

## Запуск

### Локально (без Docker)

```bash
# 1. Создать и активировать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать .env (скопируйте и отредактируйте)
cp .env.example .env   # или создайте вручную

# 4. Применить миграции
alembic upgrade head

# 5. Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# 1. Создать .env
cp env.example .env

# 2. Запустить контейнеры
docker compose up --build -d
```
