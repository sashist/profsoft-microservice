from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
    timeout=30,
)

if settings.GEMINI_API_KEY:
    embedding_client = OpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url=settings.GEMINI_BASE_URL,
        timeout=30,
    )
else:
    embedding_client = client

