from django.urls import path, include
from app.apis import CategoryAPIView, TagAPIView, PostAPIView, CommentAPIView
from rest_framework import routers

app_name = "app"

router = routers.SimpleRouter()

router.register('categories',CategoryAPIView, basename="categories")
router.register('tags',TagAPIView, basename="tags")
router.register('comments',CommentAPIView, basename="comments")
router.register('posts',PostAPIView, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]