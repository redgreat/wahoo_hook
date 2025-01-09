FROM python:3.12-alpine as requirements-stage

WORKDIR /tmp

RUN apk add --no-cache bash gcc libffi-dev musl-dev openssl-dev python3-dev \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN which poetry

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-alpine

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

COPY ./app /code
COPY ./entrypoints/entrypoints.sh /code/entrypoints.sh

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && apk del .build-deps \
    && useradd -m -d /code/app -s /bin/bash app \
    && chown -R app:app /code/app/* && chown -R app:app /code/app \
    && chmod +x entrypoints.sh

USER app

ENTRYPOINT ["/code/entrypoints.sh"]
