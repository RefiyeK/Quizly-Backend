from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Quiz
from .serializers import QuizSerializer
from .permissions import IsOwner
from .services import create_quiz_from_url


class QuizListCreateView(generics.ListCreateAPIView):
    """Listet Quizze des Benutzers auf und erstellt neue aus einer URL."""
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Gibt nur die Quizze des aktuellen Benutzers zurück."""
        return Quiz.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Nimmt eine URL entgegen und startet die Quiz-Pipeline."""
        url = request.data.get("url")
        if not url:
            return Response(
                {"detail": "URL is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        quiz = create_quiz_from_url(url, request.user)
        serializer = self.get_serializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Ruft ein einzelnes Quiz ab, aktualisiert oder löscht es."""
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Basis-Queryset für den Objektzugriff."""
        return Quiz.objects.all()