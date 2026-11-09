# 3.13 — потому что под неё гарантированно есть готовые wheel'ы для
# psycopg[binary] и pydantic-core. На 3.14 сборка может полезть компилировать
# из исходников. Если хочешь 3.14 — просто поменяй тег и пересобери.
FROM python:3.13-slim

# PYTHONUNBUFFERED=1 — критично: без него stdout буферизуется и логи
# появляются в `docker logs` с задержкой (или вообще после остановки).
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Не рутом: если кто-то пролезет через приложение, у него не будет root в контейнере.
RUN useradd --create-home --uid 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
