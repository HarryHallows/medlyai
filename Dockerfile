# Utilise Python slim image 
FROM python:3.11-slim

WORKDIR /app
COPY . /app


# Install dependencies
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic


# Create a non-root user with User ID 1000 and group 1000
RUN useradd -m -u 1000 devuser

# Change ownership of /app to devuser
RUN chown -R devuser:devuser /app

# Switch to non-root user
USER devuser

# Ensure /app is in PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8000
CMD ["sh", "/app/init_and_run.sh"]
