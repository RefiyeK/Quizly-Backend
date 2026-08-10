from django.contrib import admin

from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    """Shows questions directly in the quiz form."""
    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin configuration for quizzes with embedded questions."""
    list_display = ['id', 'title', 'owner', 'created_at']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for individual questions."""
    list_display = ['id', 'question_title', 'quiz']
