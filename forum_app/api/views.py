from rest_framework import viewsets, generics, permissions
from rest_framework.throttling import ScopedRateThrottle
from forum_app.models import Like, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionThrottle, QuestionGetThrottle, QuestionPostThrottle

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [QuestionThrottle]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_throttles(self):
        if self.action == "list" or self.action == "retrieve":
            return [QuestionGetThrottle()]

        if self.action == "create":
            return [QuestionPostThrottle()]

        return super().get_throttles()

class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "answer-scope"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
