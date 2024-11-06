FROM python:3.9

RUN apt-get update && apt-get -y install libpq-dev gcc g++ netcat-openbsd

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
RUN pip install poetry

WORKDIR /opt/service

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

COPY . .

COPY wait-for-kafka-and-ch.sh /opt/service/wait-for-kafka-and-ch.sh
RUN chmod +x /opt/service/wait-for-kafka-and-ch.sh

ENTRYPOINT ["/opt/service/wait-for-kafka-and-ch.sh"]
