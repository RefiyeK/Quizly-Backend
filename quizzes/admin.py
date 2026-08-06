from django.contrib import admin

from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    """Zeigt Fragen direkt im Quiz-Formular an."""
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin-Konfiguration für Quizze mit eingebetteten Fragen."""
    list_display = ['id', 'title', 'owner', 'created_at']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin-Konfiguration für einzelne Fragen."""
    list_display = ['id', 'question_title', 'quiz']