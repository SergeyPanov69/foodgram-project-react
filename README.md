# Учебный проект Продуктовый помощник - Foodgram

## Cайт временно(на период обучения) доступен по ссылке:
- URL: https://foodgram-serpan.mooo.com
- ip: 51.250.104.104


## О проекте
### На этом сайте пользователи, зарегистрировавшись, могут:
- публиковать рецепты,
- добавлять чужие рецепты в избранное
- подписываться на публикации других авторов.
- «cписок покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. Есть возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов.

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=blue)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=blue)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=blue)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=blue)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=blue)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=blue)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=blue)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=blue)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=blue)](https://github.com/features/actions)

## Используемые библиотеки
![python version](https://img.shields.io/badge/Python-3.9-blue)
![django version](https://img.shields.io/badge/Django-3.2.3-blue)
![django_rst version](https://img.shields.io/badge/djangorestframework-3.14.0-blue)
![djoser version](https://img.shields.io/badge/djoser-2.2.0-blue)
![psycorg version](https://img.shields.io/badge/psycopg2--binary-2.9.6-blue)
![pillow version](https://img.shields.io/badge/Pillow-9.5.0-blue)
![pyyaml version](https://img.shields.io/badge/PyYAML-6.0-blue)

### Использование Continuous Integration и Continuous Deployment (CI/CD).
При выполнении Push в ветку main репозитория GitHub выполнятся сценарии:
1. Автоматически запускаются тесты на GitHub
2. При успешном прохождении тестов, обновляются образы на Docker Hub
3. Автоматическая загрука образов с Docker Hub
4. Автоматическое разворачивание и запуск серверов в контенерах на продакшн сервере
5. В случае успеха отправка сообщения об этом в телеграмм-бот

# Как работать с репозиторием финального задания
1. Клонировать репозиторий и перейти в папку в командной строке

```
https://github.com/SergeyPanov69/foodgram-project-react/
cd foodgram_final
```

2. Запустить сервер в контейнерах
Для первого запуска, находясь в папке проекта, выполнить команду:

```
docker compose up --build
```

В скрипте (по ключу --build) автоматически выполнятся запуск серверов, миграции, подключения статики.
Последующие запуски сервера не требуют ключа --build

3. Выполнить миграции. Эта и последующие команды выполняются внутри контейнера Docker (запущен в п.2)
```
docker exec foodgram_backend python manage.py migrate
```
4. Заполнить базу данными продуктов
```
docker exec foodgram_backend python manage.py import_data
```
5. Собрать и скопировать статику
```
docker exec foodgram_backend python manage.py collectstatic
docker exec foodgram_backend cp -r collect_static/. ../static_backend/static_backend/
```
6. Создать супервользователя
```
docker exec foodgram_backend python manage.py createsuperuser
```

### Запустить в браузере

```
http://localhost:8080
```

## Автор (код Frontend)
Yandex Practicum

## Автор (код Backend) и размещение на сервере
[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://choosealicense.com/licenses/mit/)
Sergey Panov