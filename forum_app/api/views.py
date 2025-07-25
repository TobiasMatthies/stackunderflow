from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from forum_app.models import Like, Question, Answer, FileUpload
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer, FileUploadSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionThrottle, QuestionGetThrottle, QuestionPostThrottle

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [QuestionThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'author__username']
    search_fields = ['content', '^title']
    ordering_fields = ['author__username', 'category']
    ordering = ['category']

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

    def get_queryset(self):
        queryset = self.queryset
        content_param = self.request.query_params.get('content', None)

        if content_param is not None:
            queryset = queryset.filter(content__icontains=content_param)

        username_param = self.request.query_params.get('author', None)

        if username_param is not None:
            queryset = queryset.filter(author__username=username_param)

        return queryset

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


class FileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
