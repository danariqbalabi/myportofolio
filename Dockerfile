# ---- Builder stage ----
FROM python:3.13.5-alpine AS builder

WORKDIR /app

# Build deps needed to compile psycopg2 and friends
RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Runtime stage ----
FROM python:3.13.5-alpine

WORKDIR /app

# Runtime lib needed by psycopg2-binary
RUN apk add --no-cache libpq

# Bring in installed packages from the builder stage
COPY --from=builder /install /usr/local

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PRODUCTION=true

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "portofolio.wsgi:application", "--bind", "0.0.0.0:8000"]
