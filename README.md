# RAG AI Microservice (FastAPI + Qdrant + AsyncIOScheduler + Gemini)

Асинхронный RAG-микросервис (Retrieval-Augmented Generation) на базе **FastAPI**, векторной БД **Qdrant**, СУБД **PostgreSQL**, менеджера зависимостей **Poetry** и интеграции с **Google Gemini API**.

---

## ⚡ Особенности и Архитектура

- **Поиск по знаниям (RAG)**: Использование векторного поиска в Qdrant (`gemini-embedding-001`) + генерация контекстного ответа с указанием источников через `gemini-2.5-flash` (или OpenAI `gpt-4o-mini`).
- **Асинхронный воркер**: `AsyncIOScheduler` обработка документов и фоновых задач в неблокирующих `asyncio.to_thread` потоках.
- **Управление зависимостями**: Пакетный менеджер **Poetry**.
- **Миграции базы данных**: SQLAlchemy + Alembic.
- **Docker Orchestration**: Полная сборка кластера (Web, PostgreSQL, Qdrant) одной командой.

---

## 🚀 Быстрый запуск и проверка

Любой человек, склонировавший этот репозиторий, может развернуть и протестировать микросервис за 3 простых шага:

### 1. Настройка окружения
Склонируйте репозиторий и создайте `.env` из шаблона:
```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd PromtProject
cp env.example .env
```

В файле `.env` укажите ваш бесплатный ключ **Google Gemini API** (получить за 5 секунд на [Google AI Studio](https://aistudio.google.com/app/apikey)):
```env
GEMINI_API_KEY=AIzaSy...ваш_ключ_gemini...
TEST_MODE=False
```

### 2. Запуск в Docker
Запустите все сервисы (FastAPI, Qdrant, PostgreSQL):
```bash
docker compose up --build -d
```

### 3. Автоматическая загрузка тестовых данных
Выполните скрипт для заливки реалистичной базы знаний (HR, IT, безопасность, удаленка):
```bash
python scripts/seed_data.py
```

---

## 🧪 Проверка работы RAG API

### Задать вопрос по документам:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Какую сумму компания компенсирует за мобильную связь и интернет при удаленке?"}'
```

**Пример ответа**:
```json
{
  "answer": "Компания компенсирует расходы на мобильную связь и интернет в размере 2500 рублей в месяц.\nИсточник: wiki://remote-work-regulations",
  "sources": [
    {
      "source": "wiki://remote-work-regulations",
      "doc_id": 16,
      "score": 0.825
    }
  ]
}
```

### Задать вопрос НЕ по документации:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Какое расстояние от Земли до Марса?"}'
```

**Ответ системы**:
```json
{
  "answer": "В документации нет информации для ответа.",
  "sources": []
}
```

---

## 📊 Веб-интерфейс векторной базы Qdrant

Дашборд Qdrant доступен по адресу:  
🔗 [http://localhost:6333/dashboard](http://localhost:6333/dashboard)
