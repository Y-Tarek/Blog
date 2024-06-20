from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from shared.permissions import IsOwner
from app.serializers import (
    PostSerializer,
    BaseReadPostSerializer
)
from app.models import Post
from shared.utility import CsrfTokenMixin

class PostAPIView(CsrfTokenMixin,ModelViewSet):
    """ Post API View """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Post.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = ["title","content"]
    filterset_fields = [
        "categories__name",
        "tags__name",
    ]
    
    def get_queryset(self):
        return self.queryset.select_related(
            "author__user"
        ).prefetch_related(
            "categories",
            "tags",
            "post_comments"
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BaseReadPostSerializer
        return PostSerializer
    