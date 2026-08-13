# Academic Research Assistant — interactive LangGraph runtime
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860 \
    MEMORY_DB_PATH=/data/memory.db \
    USE_MOCK_LLM=true

RUN mkdir -p /data /app/data/uploads

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["sh", "-c", "uvicorn webapp:app --host 0.0.0.0 --port ${PORT:-7860}"]
