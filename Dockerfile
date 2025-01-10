FROM python:3.12 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry poetry-plugin-export

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-alpine

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
COPY ./app /code/app
COPY ./entrypoints/entrypoints.sh /code/entrypoints.sh

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && apk del .build-deps \
    && adduser -D -h /code/app app \
    && chown -R app:app /code/app && chown -R app:app /code/app/* \
    && chmod +x entrypoints.sh

USER app

ENTRYPOINT ["entrypoints.sh"]
