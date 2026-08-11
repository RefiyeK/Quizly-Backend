from rest_framework import serializers

from .models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for a question in list and detail responses."""

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Serializer for a question in the create response (with timestamps)."""

    class Meta:
        model = Question
        fields = [
            'id', 'question_title', 'question_options',
            'answer', 'created_at', 'updated_at',
        ]


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for a quiz in list and detail responses."""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description',
            'created_at', 'updated_at', 'video_url', 'questions',
        ]
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'video_url', 'questions']


class QuizCreateSerializer(QuizSerializer):
    """Serializer for the create response, using timestamped questions."""
    questions = QuestionCreateSerializer(many=True, read_only=True)
