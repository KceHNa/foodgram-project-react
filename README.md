![](https://img.shields.io/badge/Python-3.10-blue) 
![](https://img.shields.io/badge/Django-3.2-green)
![](https://img.shields.io/badge/DjangoRestFramework-3.13.1-red)
![](https://img.shields.io/badge/Docker-3.8-yellow)

# Проект Foodgram «Продуктовый помощник»

## Описание

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Как запустить проект

#### Клонировать репозиторий и перейти в него в командной строке

Можно скопировать только папку infra для серверов.

```shell
git clone git@github.com:KceHNa/foodgram-project-react.git
cd foodgram-project-react/infra
```
#### Прописать подключения в файл .env (описания см. в `.env.example`)
```bash
SECRET_KEY=your_secret_key
ALLOWED_HOSTS='*'
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
#### Добавить ip сервера в `nginx.conf`
```
server_name 127.0.0.1, <ваш_ip>;
```

#### Запустить проект 

```shell
cd ../infra
docker-compose up -d 
```
для разработчиков:
```
docker-compose up -d --build
```

#### Подготовить базу данных, статику и создать админа

```shell
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
```

## Проект доступен по следующим ссылкам:
http://84.252.137.58/

Автор бэкенда: Ксения Фурсова
