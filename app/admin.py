from django.contrib import admin


# Register your models here.
from app.models import Category, Comment, Post, Tag

class CategoryTagAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display = ["id","name","slug"]
    search_fields = ["id","name","slug"]
    ordering = ["-id"]

class PostAdmin(admin.ModelAdmin):
    @admin.display(description="author")
    def get_author(self):
        try:
          return self.author.user.email
        except:
            return None

    list_per_page=10
    list_display = ["id","title","content",get_author, "created_at", "modified_at"]
    search_fields = ["id","title"]
    ordering = ["-id"]
    list_filter = ["categories__name","tags__name"]

class CommentAdmin(admin.ModelAdmin):
    @admin.display(description="author")
    def get_author(self):
        try:
          return self.author.user.email
        except:
            return None
    
    @admin.display(description="post")
    def get_post(self):
        try:
          return self.post.title
        except:
            return None

    list_per_page=10
    list_display = ["id","content",get_author, get_post,"created_at","modified_at"]
    ordering = ["-id"]
    list_filter = ["post__title"]

admin.site.register(Category,CategoryTagAdmin)
admin.site.register(Tag,CategoryTagAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)