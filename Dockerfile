FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Configure poetry to install directly into global site-packages inside docker container
RUN poetry config virtualenvs.create false

# Copy project specification files first for caching
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy application source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
