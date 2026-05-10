# musicians-app

Веб-приложение «Музыкальное агентство» — учёт музыкантов, инструментов, концертов и выступлений.

## Стек

- Python 3.11, Flask
- PostgreSQL 16
- Pydantic для валидации
- Jinja2 + ванильный JS на клиенте

## Запуск

```
docker compose up -d
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python db\migrate.py
python run.py
```

Открыть http://127.0.0.1:5000.

## Структура

```
src/
  api/            контроллеры (Flask blueprints)
  services/       бизнес-логика
  repositories/   доступ к данным
  schemas/        Pydantic-схемы для валидации
  core/           конфиг, БД, авторизация
db/
  migrations/     SQL-миграции
static/           CSS и JS клиента
templates/        Jinja2-шаблоны
```

## API

Базовые эндпоинты задания:

- `GET /users` — список пользователей (in-memory)
- `GET /users/:id` — пользователь по id
- `POST /users` — создание пользователя

Аутентификация и доступ к данным агентства:

- `POST /api/auth/register` — регистрация
- `POST /api/auth/login` — вход, возвращает токен и данные пользователя
- `GET /api/musicians`, `POST /api/musicians`, `PUT /api/musicians/:id`, `DELETE /api/musicians/:id`
- `GET /api/concerts`, `POST /api/concerts`, `PUT /api/concerts/:id`, `DELETE /api/concerts/:id`
- `GET /api/instruments`, `POST /api/instruments`, `DELETE /api/instruments/:id`
- `GET /api/performances`, `POST /api/performances`, `DELETE /api/performances/:id`

Для всех эндпоинтов под `/api/` (кроме `/api/auth/*`) требуется заголовок `Authorization: Bearer <token>`.
Создание, изменение и удаление доступно только пользователям с ролью `admin`.

## Создание администратора

После первой регистрации пользователя выполнить:

```
psql postgresql://app:app@localhost:5432/musicians -c "CALL sp_promote_user_to_admin('<имя_пользователя>')"
```
