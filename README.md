# Quizly – Backend

Quizly is a web application that automatically generates quizzes from YouTube
videos. A user submits a YouTube URL; the backend downloads the audio,
transcribes it, and uses an AI model to create a 10-question multiple-choice
quiz. This repository contains the **backend** (Django REST API). The frontend
is a separate repository (see [Frontend](#frontend)).

## Features

- User registration, login, logout and token refresh (JWT via HttpOnly cookies)
- Quiz generation pipeline: YouTube URL → audio → transcript → AI quiz
- Quiz management: list, retrieve, partial update and delete (owner-only)
- Admin panel with inline question editing

## Tech Stack

- **Python 3.12+** (developed and tested on 3.14.3)
- Django 5.2 & Django REST Framework
- djangorestframework-simplejwt (JWT authentication)
- django-cors-headers
- yt-dlp (YouTube audio download)
- openai-whisper (speech-to-text transcription)
- google-genai (Gemini – quiz generation)

---

## System Requirements

Three tools must be installed **globally** on your system before the Python
packages. Each has a copy-paste command and a verification command below.

### 1. Python 3.12+

Check whether Python is already installed:

```
python --version
```

If it prints `Python 3.12` or higher, you are set. Otherwise install it:

- **Windows:** `winget install --id Python.Python.3.12 -e --source winget`
- **macOS:** `brew install python@3.12`
- **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install -y python3 python3-venv python3-pip`

### 2. FFMPEG

Whisper requires FFMPEG to process audio. Install it globally:

- **Windows:** `winget install --id Gyan.FFmpeg -e --source winget`
- **macOS:** `brew install ffmpeg`
- **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install -y ffmpeg`

Verify:

```
ffmpeg -version
```

### 3. Deno (required by yt-dlp)

Since 2026, yt-dlp needs an external JavaScript runtime to download from
YouTube. Deno is the recommended runtime and must be installed globally:

- **Windows:** `winget install --id DenoLand.Deno -e --source winget`
- **macOS:** `brew install deno`
- **Linux:** `curl -fsSL https://deno.land/install.sh | sh`

Verify:

```
deno --version
```

> **Windows note:** after `winget install`, close and reopen your terminal so
> that the new tools are available on the PATH.

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/RefiyeK/Quizly-Backend.git
cd Quizly-Backend
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```
python3 -m venv venv
source venv/bin/activate
```

> If PowerShell blocks the activation script, run this once, then activate
> again:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### 3. Install the dependencies

```
pip install -r requirements.txt
```

### 4. Create the `.env` file

The project reads its secrets from a `.env` file. Create it by copying the
template:

**Windows (PowerShell):**

```
Copy-Item .env.template .env
```

**macOS / Linux:**

```
cp .env.template .env
```

Now open `.env` and fill in the two values:

```
SECRET_KEY=your-django-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

**Generate a Django `SECRET_KEY`** (run this and paste the output as the value):

```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Get a free `GEMINI_API_KEY`** at https://ai.google.dev/ → "Get API key".

### 5. Run the database migrations

```
python manage.py migrate
```

### 6. Create a superuser (for the admin panel)

```
python manage.py createsuperuser
```

### 7. Start the development server

```
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`.

---

## Frontend

The frontend is a separate repository and is required to use the application
through the browser.

### 1. Clone the frontend

```
git clone https://github.com/RefiyeK/project.Quizly.git
```

### 2. Serve it on port 5500

Open the frontend folder in VS Code and start it with the **Live Server**
extension (bottom-right "Go Live"). It must run on `http://127.0.0.1:5500`.

No configuration is needed: the frontend's `config.js` already points to the
backend at `http://127.0.0.1:8000/api/`, and the backend already allows the
`http://127.0.0.1:5500` origin (CORS).

> Open the app at **http://127.0.0.1:5500** (not `localhost:5500`). The two are
> different origins for cookies; the backend is configured for `127.0.0.1`.

---

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Log in, sets auth cookies |
| POST | `/api/logout/` | Log out, blacklists refresh token |
| POST | `/api/token/refresh/` | Refresh the access token |
| GET | `/api/quizzes/` | List the current user's quizzes |
| POST | `/api/quizzes/` | Create a quiz from a YouTube URL |
| GET | `/api/quizzes/{id}/` | Retrieve a single quiz |
| PATCH | `/api/quizzes/{id}/` | Update a quiz's title/description |
| DELETE | `/api/quizzes/{id}/` | Delete a quiz |

## Authentication

Authentication uses JWT stored in **HttpOnly cookies** (`access_token` and
`refresh_token`). The access token is short-lived (5 minutes) for security; the
frontend automatically calls the refresh endpoint when it expires.

## Production Note

The cookie settings in `settings.py` are configured for local development
(`COOKIE_SECURE = False`, `COOKIE_SAMESITE = 'Lax'`). For a production
deployment served over HTTPS with a cross-site frontend, these must be changed
to `COOKIE_SECURE = True` and `COOKIE_SAMESITE = 'None'`.