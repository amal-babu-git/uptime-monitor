FROM python:3.12-alpine3.17
LABEL maintainer="amalbabu1200@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

# Install dependencies and create user
RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install --no-cache-dir -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    mkdir -p /var/run/celery && \
    chown -R app:app /vol && \
    chown -R app:app /var/run/celery && \
    chmod -R 755 /vol && \
    chmod -R 777 /var/run/celery && \
    chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

USER app

CMD ["run.sh"]