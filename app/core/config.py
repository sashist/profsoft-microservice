from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация сервиса."""

    # Строка подключения к PostgreSQL
    DATABASE_URL: str

    # URL внешнего источника данных (откуда забираем задачи)
    API_URL: str

    # URL внешнего приёмника результатов (куда отправляем ответы)
    RESULT_URL: str

    OPENAI_API_KEY: str = "test-key"
    OPENAI_BASE_URL: str | None = None
    GEMINI_API_KEY: str | None = None
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    MODEL: str = "gpt-4o-mini"
    PROMPT: str = "Определи тональность отзыва. Ответь строго одним словом: positive, negative или neutral."
    TEST_MODE: bool = False
    MAX_ATTEMPTS: int = 3
    POLL_INTERVAL: int = 5
    STUCK_MINUTES: int = 5
    RUN_WORKER: bool = True

    EMBED_MODEL: str = "text-embedding-3-small"
    EMBED_DIM: int = 1536
    CHAT_MODEL: str = "gpt-4o-mini"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 75
    TOP_K: int = 5
    MIN_RETRIEVAL_SCORE: float = 0.1
    QDRANT_URL: str = "http://qdrant:6333"
    COLLECTION: str = "docs"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
    )

settings = Settings()
