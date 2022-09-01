# Проект Foodgram «Продуктовый помощник»

## Описание

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Как запустить проект

#### Клонировать репозиторий и перейти в него в командной строке

```shell
git clone git@github.com:KceHNa/foodgram-project-react.git
cd foodgram-project-react/infra
```
#### Прописать подключения в файл .env (описания см. в `.env.example`)
```
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

#### Запустить проект 

```shell
cd ../infra
docker-compose up -d --build
```

#### Подготовить базу данных, статику и создать админа

```shell
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
```

## Проект доступен по следующим ссылкам:
http://localhost/

Автор бэкенда: Ксения Фурсова
