FROM python:3.12-alpine as requirements-stage

WORKDIR /tmp

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && apk del .build-deps

FROM python:3.12-alpine

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && apk del .build-deps \
    && useradd -m -d /src -s /bin/bash app \
    && chown -R app:app /src/* && chown -R app:app /src \
    && chmod +x entrypoints.sh

COPY ./app /code
COPY ./entrypoints/entrypoints.sh /code/entrypoints.sh

USER app

ENTRYPOINT ["/code/entrypoints.sh"]
