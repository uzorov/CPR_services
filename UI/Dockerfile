FROM node:14

WORKDIR /app

# Копируем все файлы из директории ./UI/build внутрь контейнера
COPY ./UI/dist .

EXPOSE 8000

# Запускаем сервер из директории, где находится server.js
CMD ["node", "server.js"]
