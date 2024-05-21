FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /gateway


COPY ./api-gateway/requirements.txt /gateway/
RUN pip install --no-cache-dir --upgrade -r /gateway/requirements.txt
# Перенос проекта в образ
COPY ./api-gateway/app /gateway/app

EXPOSE 8000

CMD ["/bin/sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 80"]
