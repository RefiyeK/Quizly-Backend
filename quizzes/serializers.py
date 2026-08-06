from rest_framework import serializers

from .models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer für eine einzelne Frage eines Quiz."""

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']


class QuizSerializer(serializers.ModelSerializer):
    """Serializer für ein Quiz inklusive verschachtelter Fragen."""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description',
            'created_at', 'updated_at', 'video_url', 'questions',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'video_url', 'questions']