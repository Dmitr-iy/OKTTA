# Backend OKTTA
______________________________

## Установка и запуск через докер

### Windows и Linux:
Установить и запустить докер https://www.docker.com/
После в терминале клонируете репозиторий и создаете сеть:

```
git clone https://github.com/dariedu/darieduBackend.git
cd darieduBackend
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
