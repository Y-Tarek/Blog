from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from shared.permissions import IsOwner
from app.serializers import (
    CommentSerializer,
    ReadCommentSerializer
)
from app.models import Comment
from shared.utility import CsrfTokenMixin

class CommentAPIView(CsrfTokenMixin,ModelViewSet):
    """ Comment API View """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Comment.objects.all()
   
    def get_queryset(self):
        return self.queryset.select_related(
            "author__user"
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadCommentSerializer
        return CommentSerializer
    