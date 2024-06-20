from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from shared.utility import CsrfTokenMixin
from app.serializers import (
    CategorySerializer,
    ReadCategorySerializer
)
from app.models import Category

class CategoryAPIView(ModelViewSet):
    """ Category API View """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = ["name","slug"]


    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadCategorySerializer
        return CategorySerializer
    