# EduBuild prototype backend

This backend implements the prototype flow:

```text
React -> Django -> question generator -> Django -> React
```

It intentionally has no user accounts, lesson storage, or database models.
The question generator is deterministic demo logic so the frontend flow can
be demonstrated before the Claude integration is connected.

## Run it

From `backend`:

```powershell
python -m pip install -r requirements.txt
python manage.py runserver
```

## Generate a game

Send JSON:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/generate-game/ `
  -ContentType "application/json" `
  -Body '{"text":"The water cycle includes evaporation."}'
```

The endpoint also accepts a multipart `.txt` upload in a field such as
`lesson`.

## Test

```powershell
python manage.py test
```

## What each part does

- `manage.py` is the terminal entry point for Django commands.
- `edubuild/settings.py` contains the project's configuration.
- `edubuild/urls.py` connects `/api/` to the game app.
- `games/urls.py` connects `/api/generate-game/` to the view.
- `games/views.py` receives the request, checks it, and returns JSON.
- `games/services.py` creates the two demo questions.
- `games/tests.py` sends sample requests and checks the responses.
