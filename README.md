
# Руководство по развёртыванию системы Цифровой помощник руководителя (ЦПР)

Руководство предоставляет подробные инструкции по развёртыванию системы ЦПР. 
В систему входят три основных сервиса: Сервис отправки уведомлений на почту, Сервис проверки текстов с использованием ИИ и Сервис работы с документами. Также в системе используются PostgreSQL для управления базой данных и MinIO для хранения файлов. Сервисы построены по микросервисной архитектуре с API шлюзом для авторизации запросов. Все сервисы, включая пользовательский интерфейс, упакованы в контейнеры Docker.

## Содержание
1. [Обзор](#обзор)
2. [Предварительные условия](#предварительные-условия)
3. [Методы развёртывания](#методы-развёртывания)
    - [Без локального развёртывания](#без-локального-развёртывания)
    - [Быстрое локальное развёртывание](#быстрое-локальное-развёртывание)
    - [Полное локальное развёртывание](#полное-локальное-развёртывание)
4. [Конфигурация после развёртывания](#конфигурация-после-развёртывания)
5. [Примечания](#примечания)
6. [Контакты](#контакты)

## Обзор
Система CPR Services состоит из следующих компонентов:
- **Сервис отправки уведомлений на почту**: отправляет уведомления по электронной почте через Outlook.
- **Сервис проверки текстов**: использует ИИ для проверки и исправления текстов.
- **Сервис работы с документами**: управляет операциями с документами.
- **PostgreSQL**: база данных для хранения данных.
- **MinIO**: система хранения файлов.
- **API шлюз**: управляет API запросами и авторизацией.
- **Пользовательский интерфейс**: веб-интерфейс и микрофронтенд для Сервиса проверки текстов.

## Предварительные условия
Перед началом развёртывания убедитесь, что на Вашей системе установлен Docker.

## Методы развёртывания

### Без локального развёртывания
Используйте следующие ссылки для доступа к уже развёрнутой системе в облаке:

- **Пользовательский интерфейс**: [http://176.123.163.239:8000/](http://176.123.163.239:8000/)
- **Микрофронтенд сервиса проверки текстов**: [http://176.123.163.239:8000/checker](http://176.123.163.239:8000/checker)
- **API шлюз**:
  - Базовый URL: [http://176.123.163.239:80/](http://176.123.163.239:80/)
  - API Swagger: [http://176.123.163.239:80/docs](http://176.123.163.239:80/docs)
- **Сервис работы с документами**:
  - Базовый URL: [http://176.123.163.239:83/](http://176.123.163.239:83/)
  - API Swagger: [http://176.123.163.239:83/docs](http://176.123.163.239:83/docs)
- **Сервис уведомлений**:
  - Базовый URL: [http://176.123.163.239:82/](http://176.123.163.239:82/)
- **Сервис проверки текста**:
  - Базовый URL: [http://176.123.163.239:81/](http://176.123.163.239:81/)
  - API Swagger: [http://176.123.163.239:81/](http://176.123.163.239:81/docs)
- **Панель администратора MinIO**: [http://176.123.163.239:9090/](http://176.123.163.239:9090/)
  - Логин: `minioadmin`
  - Пароль: `minioadmin`
- **PostgreSQL**: [http://176.123.163.239:5432/](http://176.123.163.239:5432/)

### Быстрое локальное развёртывание
Этот метод использует удалённые базы данных и файловое хранилище. Разворачиваются только сервисы.

1. **Клонирование репозитория**:
   ```bash
   git clone https://github.com/uzorov/CPR_services.git
   ```
2. **Переход в директорию проекта**:
   ```bash
   cd CPR_services
   ```
3. **Запуск сборки и развёртывания**:
   ```bash
   docker compose up --build -d
   ```

Время сборки зависит от скорости подключения к интернету и доступной памяти. Для успешной сборки на Windows на диске C: должно быть доступно не менее 10ГБ памяти.

#### Ускорение процесса сборки
Вы можете отключить загрузку большой модели искусственного интеллекта (около 5ГБ):
1. Откройте файл `CPR_services/text-correction-service/app/services/check_document_service.py`.
2. Закомментируйте следующие строки кода:
   ```python
   # model_long = (RuM2M100ModelForSpellingCorrection.from_pretrained(
   #   AvailableCorrectors.sage_m2m100_1B.value
   # ))
   ```

После завершения сборки система будет доступна по локальным ссылкам:
- **Пользовательский интерфейс**: [http://localhost:8000/](http://localhost:8000/)
- **Микрофронтенд сервиса проверки текстов**: [http://localhost:8000/checker](http://localhost:8000/checker)

### Полное локальное развёртывание
Для полного локального развёртывания необходимо изменить файл `docker-compose.yaml`, раскомментировав следующие строки:
```yaml
# db:
#   image: postgres:16-alpine
#   container_name: postgres
#   environment:
#     POSTGRES_DB: filesdb
#     POSTGRES_USER: postgres
#     POSTGRES_PASSWORD: uzorov
#   ports:
#     - "5432:5432"

# minio:
#   image: minio/minio:latest
#   container_name: minio
#   environment:
#     - MINIO_ROOT_USER=${MINIO_ACCESS_KEY}
#     - MINIO_ROOT_PASSWORD=${MINIO_SECRET_KEY}
#   command: server ~/minio --console-address :9090
#   ports:
#     - '9090:9090'
#     - '9000:9000'
#   volumes:
#     - minio-data:/minio
```
Для сервиса проверки текстов (document-processing-service) отредактируйте файл .env, подставив в переменные POSTGRES_URL и MINIO_URL ip адрес домашней машины. 
Затем выполните команду для сборки и развёртывания:
```bash
docker compose up --build -d
```

## Конфигурация после развёртывания

### Настройка базы данных и файлового хранилища
1. Перейдите в директорию `CPR_services/document-processing-service` и выполните миграции в базу данных:
   ```bash
   alembic upgrade head
   ```

Если миграция завершилась с ошибкой из-за сброса подключения, измените ссылку на базу данных, отредактировав файл `alembic.ini`:
```ini
63 sqlalchemy.url = postgresql://postgres:uzorov@localhost:5432/filesdb
```
Подставьте IP-адрес вашего компьютера (его можно узнать командой `ipconfig` в cmd).

2. Настройка файлового хранилища:
   - Перейдите по ссылке: [http://localhost:9090/](http://localhost:9090/)
   - Логин: `minioadmin`
   - Пароль: `minioadmin`
   - Создайте новый bucket с названием `files`.
   - В настройках bucket разрешите анонимный доступ.

После выполнения этих шагов система будет полностью развёрнута и готова к работе.


## Примечания
Для работы сервиса уведомлений необходимы логин и пароль от учётной записи Outlook. Во избежание потери данных учётной записи, поля логин и пароль в Сервисе уведомлений отсутствуют. По этой причине письма в развёрнутом вариание Системы не отправляются. Для локальной настройки необходимо добавить логин и пароль в настройки приложения, после чего пересобрать контейнер с сервисом.

При удалённом доступе к Системе возникнут трудности с использованием функции голосвого ввода - это происходит из-за того, что браузеры блокируют доступ к микрофону при незащищённом соединении (http). По этой причине для тестирования данной функции необходимо локальное развёртывание Cервиса.

Микрофронтенд для Сервиса проверки текстов = это отдельное приложение, которое позволяет оценить все три подхода, реализованных в ходе разработки проекта, с удобным пользовательским интерфейсом (см. рисунок ниже).

![image](https://github.com/uzorov/CPR_services/assets/90005421/a16c4343-86b1-41c7-a765-a2a0500bbc9d)


## Контакты
При возникновении сложностей можно писать в Telegram: [@uzorovk](https://t.me/uzorovk)

