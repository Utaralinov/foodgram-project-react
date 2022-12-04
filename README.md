![foodgram workflow](https://github.com/Utaralinov/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
# Foodgram

## Автор проекта студент факультета Бэкенд: Утаралинов Нурсултан

### Примеры запросов:
http://158.160.14.23/api/

# Запуск проекта
## Запуск проекта в dev-режиме без Docker
### Клонировать репозиторий и перейти в него в командной строке:
#### HTTPS
```
git clone https://github.com/Utaralinov/foodgram-project-react.git
```
#### SSH
```
git clone git@github.com:Utaralinov/foodgram-project-react.git
```
#### GitHub CLI
```
git clone gh repo clone Utaralinov/foodgram-project-react
```
### Создайте и активируйте виртуальное окружение
```
python -m venv venv
```
```
. venv/Scripts/activate
```
### Обновите pip
```
python -m pip install --upgrade pip
```
### Перейдите (команда cd ...) в папку с файлом requirements.txt и установите зависимостси
```
pip install -r requirements.txt
```
## Шаблоны наполнения env-файла:
В директорий infra создайте файл .env с переменными окружения для базы данных

<code>
DB_ENGINE=django.db.backends.postgresql #Указываем, что работаем с postgresql
DB_NAME=postgres #Имя базы данных
POSTGRES_USER=postgres_user #Логин для подключения к базе данных
POSTGRES_PASSWORD=postgres_password #Пароль для подключения к БД (установите свой)
DB_HOST=db_host #Название сервиса (контейнера)
DB_PORT=1234 #Порт для подключения к БД
SECRET_KEY='Ваш секретный ключ проекта'
</code>

###  Запуск
Из папки infra/ разверните контейнеры при помощи docker-compose
<code>$ docker-compose up -d --build</code>

Выполните миграции
<code>$ docker-compose exec web python manage.py migrate</code>

Создайте суперпользователя
<code>$ docker-compose exec web python manage.py createsuperuser</code>

Соберите статику
<code>$ docker-compose exec web python manage.py collectstatic --no-input</code>

Разместив файл fixtures.json в папке с Dockerfile, можно загрузить в базу данные из дампа:
<code>$ docker-compose exec web python manage.py loaddata fixtures.json</code>

Остановка проекта:
<code>$ docker-compose down</code>
