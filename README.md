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
docker-compose up -d --build
```

#### Подготовить базу данных, статику и создать админа

```shell
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
```
Базу можно наполнить несколькими способами, например:
```bash
sudo -u postgres psql
```
```sql
\copy public.recipes_ingredient (name, measurement_unit) FROM '/<you_dir_project>/data/ingredients.csv' DELIMITER ',' CSV ENCODING 'UTF8' QUOTE '\"' ESCAPE '''';""
```
Или подключиться через PgAdmin - Import Data

## Проект доступен по следующим ссылкам:
http://84.252.137.58/

Login admin: `kcehna@me.com`
Pass: `kcehna@me.comkcehna@me.com`
http://84.252.137.58/admin

Автор бэкенда: Ксения Фурсова
