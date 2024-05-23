FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /text-correction-service

COPY ./text-correction-service/requirements.txt /text-correction-service/
RUN pip install --no-cache-dir -r /text-correction-service/requirements.txt

COPY ./text-correction-service/app /text-correction-service/app

RUN cd /text-correction-service/app/sage && \
    pip install . && \
    pip install -e .[errant]

EXPOSE 81

CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port 81"]
