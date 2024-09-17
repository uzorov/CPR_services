@echo off

@REM REM Логинимся в Docker Hub
@REM docker login -u uzorovkirill -p Rekid2000

@REM REM Собираем образы
docker-compose build

@REM REM Отправляем образы в Docker Hub
@REM docker push uzorovkirill/correct-text-ai:latest
@REM docker push uzorovkirill/document-processing-service:latest
@REM REM docker push cpr-ui.cr.cloud.ru/cpr-web-ui:latest
@REM docker push uzorovkirill/api-gateway:latest

docker login cpr-web-ui.cr.cloud.ru -u b110a0a98fb8aa4f8840167b19f86177 -p e46e6f1abdec564745d7f16fd4d41c66

docker push cpr-web-ui.cr.cloud.ru/cpr-web-ui:latest

echo All images successfully sent to Docker Hub
pause
