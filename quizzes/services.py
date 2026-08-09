import os
import json
import tempfile
import uuid
import re
from .models import Quiz, Question

import yt_dlp
import whisper
from google import genai


def download_audio(url):
    """Lädt das Audio eines YouTube-Videos herunter und gibt den Dateipfad zurück."""
    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename


def transcribe_audio(audio_path):
    """Transkribiert eine Audiodatei mit Whisper und gibt den Text zurück."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]


def generate_quiz_from_transcript(transcript):
    """Erzeugt aus einem Transkript ein Quiz im JSON-Format mit Gemini."""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    prompt = _build_prompt(transcript)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return _parse_quiz_json(response.text)


def _build_prompt(transcript):
    """Baut den Prompt für die Quiz-Generierung aus dem Transkript."""
    return (
        "Based on the following transcript, generate a quiz in valid JSON "
        "format. The quiz must follow this exact structure:\n"
        '{"title": "A concise quiz title based on the transcript topic.", '
        '"description": "Summarize the transcript in max 150 characters. '
        'No quiz questions or answers.", '
        '"questions": [{"question_title": "The question.", '
        '"question_options": ["Option A", "Option B", "Option C", "Option D"], '
        '"answer": "The correct option, exactly matching one of the options"}]}\n'
        "Requirements:\n"
        "- Exactly 10 questions.\n"
        "- Each question has exactly 4 distinct options.\n"
        "- Only one correct answer, must be present in question_options.\n"
        "- Output valid JSON, parsable by json.loads. No text outside JSON.\n\n"
        "Transcript:\n" + transcript
    )


def _parse_quiz_json(raw_text):
    """Bereinigt die KI-Antwort und parst sie als JSON."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned.strip())


def create_quiz_from_url(url, user):
    """Führt die komplette Pipeline aus und speichert das Quiz für den Benutzer."""
    audio_path = download_audio(url)
    transcript = transcribe_audio(audio_path)
    quiz_data = generate_quiz_from_transcript(transcript)
    return _save_quiz(quiz_data, url, user)


def _save_quiz(quiz_data, url, user):
    """Speichert Quiz und Fragen in der Datenbank."""
    quiz = Quiz.objects.create(
        owner=user,
        title=quiz_data["title"],
        description=quiz_data["description"],
        video_url=_normalize_youtube_url(url),
    )
    for question in quiz_data["questions"]:
        Question.objects.create(
            quiz=quiz,
            question_title=question["question_title"],
            question_options=question["question_options"],
            answer=question["answer"],
        )
    return quiz


def _normalize_youtube_url(url):
    """Extrahiert die Video-ID und baut die kanonische YouTube-URL."""
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if match:
        return f"https://www.youtube.com/watch?v={match.group(1)}"
    return url
