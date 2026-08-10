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

- **Python 3.14** (developed and tested on 3.14.3)
- Django 5.2 & Django REST Framework
- djangorestframework-simplejwt (JWT authentication)
- django-cors-headers
- yt-dlp (YouTube audio download)
- openai-whisper (speech-to-text transcription)
- google-genai (Gemini – quiz generation)

## System Requirements

Before installing the Python packages, the following tools must be installed
**globally** on your system:

### FFMPEG (required)

Whisper requires FFMPEG to process audio. It must be installed globally and be
available on the system PATH.

- **Windows:** `winget install --id Gyan.FFmpeg -e --source winget`
- **macOS:** `brew install ffmpeg`

Verify the installation:

```
ffmpeg -version
```

### Deno (required for yt-dlp)

Since 2026, yt-dlp needs an external JavaScript runtime to download from
YouTube. Deno is the recommended runtime and must be installed globally.

- See: https://deno.com

Verify the installation:

```
deno --version
```

## Installation

1. **Clone the repository**

   ```
   git clone https://github.com/RefiyeK/Quizly-Backend.git
   cd Quizly-Backend
   ```

2. **Create and activate a virtual environment**

   Windows (PowerShell):

   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   macOS / Linux:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Create the `.env` file**

   Copy `.env.template` to `.env` and fill in your own values:

   ```
   SECRET_KEY=your-django-secret-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

   A free Gemini API key can be created at https://ai.google.dev/.

5. **Run the database migrations**

   ```
   python manage.py migrate
   ```

6. **Create a superuser** (to access the admin panel)

   ```
   python manage.py createsuperuser
   ```

7. **Start the development server**

   ```
   python manage.py runserver
   ```

   The API is now available at `http://127.0.0.1:8000/api/`.

## Frontend

The frontend is a separate repository and is required to use the application
through the browser. Fork or clone it from:

- https://github.com/RefiyeK/project.Quizly

Run the frontend with a static server (e.g. the VS Code **Live Server**
extension) on `http://127.0.0.1:5500`. The backend is preconfigured to allow
this origin (CORS).

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