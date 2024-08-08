#!/bin/sh

# Настроим переменные окружения для базы данных
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

# Добавим путь к Python
export PYTHONPATH=/file-processing-service/app

# Печатаем переменные окружения для диагностики
echo "DATABASE_URL=${DATABASE_URL}"
echo "PYTHONPATH=${PYTHONPATH}"

# Печатаем список файлов в директории приложения для диагностики
ls -R /file-processing-service/app

# Создадим временный файл конфигурации Alembic с подставленными значениями переменных окружения
cat > /file-processing-service/app/alembic_temp.ini <<EOL
[alembic]
script_location = /file-processing-service/app/alembic

sqlalchemy.url = ${DATABASE_URL}

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers = console
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers = console
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
EOL

# Печатаем временный файл конфигурации для диагностики
cat /file-processing-service/app/alembic_temp.ini

# Выполним миграции Alembic, используя временный файл конфигурации
alembic -c /file-processing-service/app/alembic_temp.ini upgrade head

# Запустим основной процесс приложения
exec "$@"
