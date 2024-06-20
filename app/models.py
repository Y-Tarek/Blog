from shared.models import TimeStampedWithNamesModel,TimeStampModel
from users.models import Profile
from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(TimeStampedWithNamesModel):
    """ The Category Model """

    class Meta:
        """Class meta for Category model."""
        ordering = ["-id"]
        verbose_name = _("Category")
        verbose_name_plural = _("Category")
    

class Tag(TimeStampedWithNamesModel):
    """ The Tag Model """

    class Meta:
        """Class meta for Tag model."""
        ordering = ["-id"]
        verbose_name = _("Tag")
        verbose_name_plural = _("Tag")


class Post(TimeStampModel):
    """ The Post Model """

    author = models.ForeignKey(Profile, related_name="profile_posts", on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category,related_name="post_categories")
    tags = models.ManyToManyField(Tag,related_name="post_tags")
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        """Class meta for Post model."""
        ordering = ["-id"]
        verbose_name = _("Post")
        verbose_name_plural = _("Post")
    
    def __str__(self):
        return self.title

class Comment(TimeStampModel):
    """ The Comment Model """

    author = models.ForeignKey(Profile, related_name="profile_comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_comments", on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        """Class meta for Comment model."""
        ordering = ["-id"]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comment")
    
    def __str__(self):
        return str(self.id)