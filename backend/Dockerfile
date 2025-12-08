FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render automatically provides PORT environment variable
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}