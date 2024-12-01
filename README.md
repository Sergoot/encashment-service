# Encashment Service
# ВЕРСИЯ 0.0.1
Моно-репозиторий со всеми сервисами проекта

Scrum: https://sergeylyutavin22.kaiten.ru/space/449927

### Запуск backend
**Перед запуском бэка у вас должен быть установлен docker**
- У каждого бек-сервиса свои зависимости на poetry и свои .env файлы
- Перед запуском необходимо создать .env файлы в каждом сервисе
    `cp .env.example > .env`
    и заполнить своими данными если нужно
- Запустить все сервисы сразу можно командой
    `docker compose --env-file .env.deploy up --build`

### Запуск frontend
**Перед запуском фронта у вас должна быть установлена Node.js 18+ версии**
- `cd frontend`, там запускеете `npm i`
- затем `npm run dev`
- приложение запускается на дефолтном localhost с портом 5173
=======
- Схема сервисов
  ![telegram-cloud-photo-size-2-5213088256160293610-y](https://github.com/user-attachments/assets/848d0103-59c6-4598-95d7-11f84d7ab27d)