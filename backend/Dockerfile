# Build from repo root: docker build -f backend/Dockerfile .
FROM python:3.12-slim

WORKDIR /app

# Install dependencies (requirements at repo root in build context)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code (overridden by volume mount when using docker-compose with live reload)
COPY backend .

EXPOSE 8001

# --reload so that mounted source changes are picked up in development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
