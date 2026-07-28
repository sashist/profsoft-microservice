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
    MODEL: str = "gpt-4o-mini"
    PROMPT: str = "Определи тональность отзыва. Ответь строго одним словом: positive, negative или neutral."
    TEST_MODE: bool = False
    MAX_ATTEMPTS: int = 3
    POLL_INTERVAL: int = 5
    STUCK_MINUTES: int = 5
    RUN_WORKER: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
    )

settings = Settings()
