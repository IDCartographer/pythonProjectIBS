FROM python:3.10-buster
WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .

ENV POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=aB89027311 \
    POSTGRES_HOST=host.docker.internal \
    POSTGRES_PORT=5432 \
    POSTGRES_DB=postgres
RUN sed -i 's/localhost/host.docker.internal/g' main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

