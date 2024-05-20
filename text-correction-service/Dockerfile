FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /text-correction-service

COPY ./requirements.txt /text-correction-service/
RUN pip install --no-cache-dir -r /text-correction-service/requirements.txt

COPY ./app /text-correction-service/app

EXPOSE 85

CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port 85"]
