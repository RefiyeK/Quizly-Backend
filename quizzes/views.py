from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Quiz
from .serializers import QuizSerializer
from .permissions import IsOwner
from .services import create_quiz_from_url


class QuizListCreateView(generics.ListCreateAPIView):
    """List the user's quizzes and create new ones from a URL."""
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the quizzes of the current user."""
        return Quiz.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Accept a URL and start the quiz pipeline."""
        url = request.data.get("url")
        if not url:
            return Response(
                {"detail": "URL is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            quiz = create_quiz_from_url(url, request.user)
        except Exception:
            return Response(
                {"detail": "Quiz could not be generated from the given URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single quiz."""
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Base queryset for object access."""
        return Quiz.objects.all()
