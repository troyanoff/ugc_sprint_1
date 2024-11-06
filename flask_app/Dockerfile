FROM python:3.10-slim-buster

RUN apt-get update && apt-get -y install libpq-dev gcc g++ && \
    apt-get install -y nmap ncat

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
RUN pip install poetry

WORKDIR /flask_app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

# Установите зависимости
RUN poetry config virtualenvs.create false
RUN poetry install
# RUN poetry install --no-interaction --no-dev

COPY wait-for-kafka.sh wait-for-kafka.sh
RUN chmod +x wait-for-kafka.sh

EXPOSE 5000

COPY . .

CMD ["./wait-for-kafka.sh"]
    