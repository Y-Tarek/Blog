from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from app.serializers import (
    TagSerializer,
    ReadTagSerializer
)
from app.models import Tag
from shared.utility import CsrfTokenMixin

class TagAPIView(CsrfTokenMixin,ModelViewSet):
    """ Tag API View """
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = ["name","slug"]
    

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadTagSerializer
        return TagSerializer
    