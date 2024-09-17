@echo off

@REM REM Логинимся в Docker Hub
@REM docker login -u -p 

@REM REM Собираем образы
docker-compose build

@REM REM Отправляем образы в Docker Hub
@REM docker push uzorovkirill/correct-text-ai:latest
@REM docker push uzorovkirill/document-processing-service:latest
@REM REM docker push cpr-ui.cr.cloud.ru/cpr-web-ui:latest
@REM docker push uzorovkirill/api-gateway:latest

docker login cpr-web-ui.cr.cloud.ru -u  -p 

docker push cpr-web-ui.cr.cloud.ru/cpr-web-ui:latest

echo All images successfully sent to Docker Hub
pause
