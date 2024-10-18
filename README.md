# Encashment Service

Моно-репозиторий со всеми сервисами проекта

Scrum: https://sergeylyutavin22.kaiten.ru/space/449927

### Запуск
- У каждого бек-сервиса свои зависимости на poetry и свои .env файлы
- Перед запуском необходимо создать .env файлы в каждом сервисе
    `cp .env.example > .env`
    и заполнить своими данными если нужно
- Запустить все сервисы сразу можно командой
    `docker compose --env-file .env.deploy up --build`

- Схема сервисов
  ![telegram-cloud-photo-size-2-5213088256160293610-y](https://github.com/user-attachments/assets/848d0103-59c6-4598-95d7-11f84d7ab27d)
