# Backend OKTTA

<img alt="Static Badge" src="https://img.shields.io/badge/Python-3.10-brightgreen?style=plastic&logo=python&logoColor=green">  <img alt="Static Badge" src="https://img.shields.io/badge/rest_framework-3.14-brightgreen?style=plastic&logo=django&logoColor=green&cacheSeconds=3600"> <img alt="Static Badge" src="https://img.shields.io/badge/postgreSQL-14-brightblue?style=plastic&logo=postgresql&logoColor=blue&labelColor=grey&color=blue&cacheSeconds=3600"> 

![DjangoREST](https://img.shields.io/badge/DJANGO-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
______________________________
## Админ регистрируется в системе, получает доступ к управлению дашборда.

- Создавать интеграции: Telegram, WhatsApp, ВКонтакте

- После интеграции система создает чат

- Статистика обращений в чат пользователей за текущий день, неделю, месяц
- Настройки Gpt

- Добавлять менеджера. Добавление через email, статус активный становится после подтверждения эл. почты. Менеджер имеет домтуп только к чатам админа.
- Приобретать тарифный план

______________________________
______________________________
## Установка и запуск через докер

### Windows и Linux:
Установить и запустить докер https://www.docker.com/
После в терминале клонируете репозиторий и создаете сеть:

```
https://github.com/Dmitr-iy/OKTTA.git
cd OKTTA
docker network create mynetwork
```

В папку OKTTA/OKTTA кладете файл .env, потом в терминале из директории OKTTA/OKTTA запускаете докер:
```
docker-compose up
```

В приложении Docker должен появиться контейнер dariedubackend, в нем должно выполняться (running) два процесса: db и dariedu-server.
Возможно, вместо docker-compose сработает docker compose.
Выход: Ctrl+C

При последующих запусках для обновления файлов:
```
git pull
```

И далее перезапуск докера:
```
docker-compose up --build
```

Для создания админа (суперпользователя), для доступа в админ панель, при запущенном докере в соседнем терминале из директории OKTTA/OKTTA:
```
docker-compose exec -ti oktta-server python manage.py createsuperuser
```
Вводить email, пароль дважды (при введении пароль не отображается), если говорит, что пароль слишком простой/короткий, пишете Y, готово.
__________________________________________

Сервер с API запустится по адресу http://127.0.0.1:8000/api
swagger: http://127.0.0.1:8000/api/swagger
админ-панель: http://127.0.0.1:8000/admin здесь нужно ввести данные админа (суперпользователя).

Для просмотра логов:
```
docker logs oktta-oktta-server-1
```

данные необходимые в .env

```
SECRET_KEY= 'ключ Django'

BASE_URL='url перенаправления после подтверждения email' на локальном: http://localhost:8000
# при локальном развертывании для работы webhook
WEBHOOK_URL='адрес ngrok'  
TELEGRAM_URL=https://api.telegram.org/bot

DB_NAME=
DB_USER=
DB_PASSWORD=

## for local
#DB_HOST=localhost
#DB_PORT=5432

## for docker
DB_HOST=db
DB_PORT=
BACKEND_DB_PORT=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```
