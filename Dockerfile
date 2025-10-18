FROM python:3.11-slim

WORKDIR /app

# Avoid cache for pip if you change requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "src.app.demo_api:app", "--host", "0.0.0.0", "--port", "8000"]
