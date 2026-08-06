import re


def _split_long_part(part: str, size: int) -> list[str]:
    words = part.split()
    if not words:
        return []

    chunks: list[str] = []
    current: list[str] = []

    for word in words:
        candidate = " ".join([*current, word])
        if len(candidate) <= size:
            current.append(word)
        else:
            if current:
                chunks.append(" ".join(current))
            current = [word]

    if current:
        chunks.append(" ".join(current))

    return chunks


def _tail_for_overlap(text: str, overlap: int) -> str:
    if overlap <= 0 or not text:
        return ""

    words = text.split()
    selected: list[str] = []
    total_len = 0

    for word in reversed(words):
        added_len = len(word) if not selected else len(word) + 1
        if total_len + added_len > overlap:
            break
        selected.append(word)
        total_len += added_len

    return " ".join(reversed(selected))


def split_text(text: str, size: int, overlap: int) -> list[str]:
    if not text or size <= 0:
        return []

    normalized = re.sub(r"\r\n?", "\n", text).strip()
    if not normalized:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", normalized) if p.strip()]
    parts: list[str] = []

    for paragraph in paragraphs:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", paragraph) if s.strip()]
        if not sentences:
            continue
        for sentence in sentences:
            if len(sentence) <= size:
                parts.append(sentence)
            else:
                parts.extend(_split_long_part(sentence, size))

    if not parts:
        return []

    chunks: list[str] = []
    current = ""

    for part in parts:
        candidate = part if not current else f"{current} {part}"
        if len(candidate) <= size:
            current = candidate
            continue

        if current:
            chunks.append(current)
            tail = _tail_for_overlap(current, overlap)
            current = part if not tail else f"{tail} {part}"
        else:
            current = part

        while len(current) > size:
            splitted = _split_long_part(current, size)
            if not splitted:
                break
            chunks.append(splitted[0])
            tail = _tail_for_overlap(splitted[0], overlap)
            rest = " ".join(splitted[1:]).strip()
            current = rest if not tail or not rest else f"{tail} {rest}"
            if not rest:
                current = ""
                break

    if current:
        chunks.append(current)

    return chunks
