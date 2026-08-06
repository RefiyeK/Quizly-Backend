from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Quiz
from .serializers import QuizSerializer
from .permissions import IsOwner


class QuizListView(generics.ListAPIView):
    """Listet alle Quizze des angemeldeten Benutzers auf."""
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Gibt nur die Quizze des aktuellen Benutzers zurück."""
        return Quiz.objects.filter(owner=self.request.user)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Ruft ein einzelnes Quiz ab, aktualisiert oder löscht es."""
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Basis-Queryset für den Objektzugriff."""
        return Quiz.objects.all()
