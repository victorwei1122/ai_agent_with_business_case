FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies needed for psycopg2 compilation if necessary (though we use binary)
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config.yml .

EXPOSE 8000

# Sleep for a few seconds to let Postgres start up, then seed db, then run server
CMD ["sh", "-c", "sleep 5 && python -m src.db.seed_db && uvicorn src.api:app --host 0.0.0.0 --port 8000"]
