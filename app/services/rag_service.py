from app.ai.client import client, embedding_client
from app.core.config import settings
from app.services.retrieval import search


SYSTEM_PROMPT = """Ты отвечаешь на вопрос только по переданному контексту.
Если в контексте нет ответа, прямо скажи: «В документации нет информации для ответа».
Не используй внешние знания и не придумывай факты.
В конце ответа обязательно укажи источник в формате: Источник: <source>."""


def answer(question: str) -> dict:
    points = search(question, settings.TOP_K)
    relevant_points = [
        point for point in points if point.score >= settings.MIN_RETRIEVAL_SCORE
    ]
    sources = []
    context_parts = []

    for point in relevant_points:
        payload = point.payload or {}
        source = payload.get("source", "unknown")
        section = payload.get("section")
        text = payload.get("text", "")

        sources.append(
            {
                "source": source,
                "doc_id": payload.get("doc_id"),
                "section": section,
                "text": text,
                "score": point.score,
            }
        )
        context_parts.append(f"[Источник: {source}; секция: {section}]\n{text}")

    if not context_parts:
        return {
            "answer": "В документации нет информации для ответа",
            "sources": [],
        }

    context = "\n\n".join(context_parts)
    if settings.TEST_MODE:
        return {
            "answer": f"Тестовый режим. {sources[0]['text']}\n\nИсточник: {sources[0]['source']}",
            "sources": sources,
        }

    chat_client = embedding_client if settings.CHAT_MODEL.startswith("gemini") else client

    response = chat_client.chat.completions.create(
        model=settings.CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Контекст:\n{context}\n\nВопрос: {question}",
            },
        ],
    )

    return {
        "answer": (response.choices[0].message.content or "").strip(),
        "sources": sources,
    }
