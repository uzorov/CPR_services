FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /file-processing-service

COPY document-processing-service/requirements.txt /file-processing-service/
RUN pip install --no-cache-dir -r /file-processing-service/requirements.txt

COPY document-processing-service/.env /file-processing-service/.env

COPY document-processing-service/app /file-processing-service/app

COPY document-processing-service/app/entrypoint.sh /file-processing-service/app/entrypoint.sh

COPY document-processing-service/app/alembic /file-processing-service/app/alembic
COPY document-processing-service/app/alembic.ini /file-processing-service/app/alembic.ini

ENV ALEMBIC_CONFIG=/file-processing-service/app/alembic.ini

RUN chmod +x /file-processing-service/app/entrypoint.sh

EXPOSE 83

ENTRYPOINT ["/file-processing-service/app/entrypoint.sh"]
CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port 83"]