FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /file-processing-service

COPY ./requirements.txt /file-processing-service/
RUN pip install --no-cache-dir -r /file-processing-service/requirements.txt

COPY ./.env /file-processing-service/.env



COPY ./app /file-processing-service/app

COPY ./app/alembic /file-processing-service/app/alembic
COPY ./app/alembic.ini /file-processing-service/app/alembic.ini

EXPOSE 82

CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port 82"]
