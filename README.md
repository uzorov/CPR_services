
---
 

### ⚠️ ВАЖНО

**Информация в данном руководстве устарела**. Инструкцию по полному развёртыванию системы см. в репозитории: **"Руководство по полному развёртыванию сервисов ЦПР.pdf"**

 
---


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
5. [Контакты](#контакты)

## Обзор
Система CPR Services состоит из следующих компонентов:
- **Сервис работы с ИИ**: использует ИИ для проверки и исправления текстов, а также транскрибации аудио.
- **Сервис работы с документами**: управляет операциями с документами.
- **PostgreSQL**: база данных для хранения данных.
- **MinIO**: система хранения файлов.
- **API шлюз**: управляет API запросами и авторизацией.
- **Keycloak**: авторизует пользователей и выдаёт роли
- **Пользовательский интерфейс**: веб-интерфейс.

## Предварительные условия
Перед началом развёртывания убедитесь, что на Вашей системе установлен Docker.

## Методы развёртывания

### Без локального развёртывания
Используйте следующие ссылки для доступа к уже развёрнутой системе в облаке:

- **Пользовательский интерфейс**: [https://cpr-ui.containers.cloud.ru](http://176.123.163.239:8000/)

### Быстрое локальное развёртывание
Этот метод использует удалённые базы данных и файловое хранилище. Разворачиваются только сервисы.

1. **Клонирование репозитория**:
   ```bash
   git clone https://github.com/uzorov/CPR_services.git
   ```
2. **Переход в директорию проекта**:
   ```bash
   cd CPR_services/images
   ```
3. **Запуск сборки и развёртывания**:
   ```bash
   docker compose up --build -d
   ```

Время сборки зависит от скорости подключения к интернету и доступной памяти. Для успешной сборки на Windows на диске C: должно быть доступно не менее 15ГБ памяти.

После завершения сборки система будет доступна по локальным ссылкам:
- **Пользовательский интерфейс**: [http://localhost:8000/](http://localhost:8000/)

### Полное локальное развёртывание
Для полного локального развёртывания необходимо изменить файл `docker-compose.yaml`, раскомментировав все строки:
```yaml
# version: '3'

# services:

  # keycloak:
  #   image: quay.io/keycloak/keycloak:23.0.1
  #   ports:
  #     - "8080:8080"
  #   environment:
  #     - KEYCLOAK_ADMIN=admin
  #     - KEYCLOAK_ADMIN_PASSWORD=admin
  #   command:
  #     - "start-dev"

  # ai-service:
  #   build:
  #     context: .
  #     dockerfile: ai-service/Dockerfile
  #   ports:
  #     - "84:84"

  # notification-service:
  #   build:
  #     context: .
  #     dockerfile: notification-service/NotificationService/Dockerfile
  #   ports:
  #     - "82:82"
    
  # db:
  #   image: postgres:16-alpine
  #   container_name: postgres
  #   environment:
  #     POSTGRES_DB: filesdb
  #     POSTGRES_USER: postgres
  #     POSTGRES_PASSWORD: uzorov
  #   ports:
  #     - "5432:5432"
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data

  # document-processing-service:
  #   build:
  #     context: .
  #     dockerfile: document-processing-service/Dockerfile
  #   ports:
  #     - "83:83"
  #   environment:
  #     POSTGRES_DB: filesdb
  #     POSTGRES_USER: postgres
  #     POSTGRES_PASSWORD: uzorov
  #     POSTGRES_HOST: 87.242.86.68
  #     POSTGRES_PORT: 5432
    # depends_on:
    #   - db


  # web-interface:
  #   build:
  #     context: .
  #     dockerfile: UI/Dockerfile
  #   ports:
  #     - "8000:8000"

  # gateway:
  #   build:
  #     context: .
  #     dockerfile: api-gateway/Dockerfile
  #   ports:
  #     - "80:80"

  # db:
  #   image: postgres:16-alpine
  #   container_name: postgres
  #   environment:
  #     POSTGRES_DB: filesdb
  #     POSTGRES_USER: postgres
  #     POSTGRES_PASSWORD: uzorov
  #   ports:
  #     - "5432:5432"
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data  
  #   entrypoint:
  #     - /entrypoint.sh

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

# volumes:
#   postgres_data:
  # minio-data:

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


## Контакты
При возникновении сложностей можно писать в Telegram: [@uzorovk](https://t.me/uzorovk)

