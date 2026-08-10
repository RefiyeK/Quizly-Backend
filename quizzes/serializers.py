from rest_framework import serializers

from .models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for a single question of a quiz."""

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for a quiz including nested questions."""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description',
            'created_at', 'updated_at', 'video_url', 'questions',
        ]
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'video_url', 'questions']
