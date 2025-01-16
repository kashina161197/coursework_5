FROM python:3.12 AS builder

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --verbose && poetry show

COPY . .


ENV SECRET_KEY="django-insecure-w36)6(_37%+k-g^sgcl(*^i&!8c=4*0!176q6asjemyulf1@y1"
ENV CELERY_BROKER_URL="redis://localhost:6379/0"
ENV CELERY_BACKEND="redis://localhost:6379/0"
ENV PYTHONPATH="/app"

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
