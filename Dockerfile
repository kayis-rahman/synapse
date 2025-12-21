FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag/ ./rag/
COPY rag_server/ ./rag_server/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "rag_server.main:app", "--host", "0.0.0.0", "--port", "8000"]