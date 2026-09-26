FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 1000 appuser

ENV APP_NAME="Order / Cargo stub" \
    CACHE_TTL_SECONDS=10800 \
    RESPONSE_DELAY_MS=500

COPY app.py .

USER appuser

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
