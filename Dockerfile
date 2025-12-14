FROM python:3.11-slim

WORKDIR /app
COPY . /app



RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic

ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8000


CMD ["sh", "/app/init_and_run.sh"]
