FROM node:14

WORKDIR /app

# Копируем все файлы из директории ./UI/build внутрь контейнера
COPY ./UI-taskmanager/task-manager/package*.json ./
RUN npm install

ARG VUE_APP_GATEWAY_URL

ENV VUE_APP_GATEWAY_URL=${VUE_APP_GATEWAY_URL}
COPY ./UI-taskmanager/task-manager ./
RUN npm run build

WORKDIR /app/dist

COPY ./UI/dist/server.js .

EXPOSE 8000

# Запускаем сервер из директории, где находится server.js
CMD ["node", "server.js"]
