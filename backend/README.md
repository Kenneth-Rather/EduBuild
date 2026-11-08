# EduBuild database

The backend is a Django project. The local development database is SQLite at
`backend/db.sqlite3`; it is intentionally ignored by Git. Django migrations
are the source of truth for creating the schema.

## Start the backend

From `backend` in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/admin/> and sign in with the superuser. The
`games` app is registered there so lessons, games, generation requests, game
versions, questions, and share links can be inspected without a frontend.

## Database workflow

When a model changes:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Run the database tests with:

```powershell
python manage.py test games
```

The schema deliberately does not store student accounts or answers. A
`ShareLink` lets students open a published game without storing student
personal data.

## Separate prototype database

The requested minimal schema is in a separate SQLite file:
`backend/prototype_db.sqlite3`.

It contains:

- `users`: `id`, `email`, `password`, `created_at`
- `generation_requests`: `id`, `user_id`, `grade`, `subject`, `genre`,
  `difficulty`, `uploaded_text`, `created_at`
- `games`: `id`, `user_id`, `request_id`, `title`, `game_json`, `created_at`

Create or update that database with:

```powershell
python manage.py migrate --database=prototype
```

Use the models through the `prototype` database alias:

```python
from prototype_db.models import Game

games = Game.objects.using("prototype").all()
```

This database is independent from `backend/db.sqlite3`.
