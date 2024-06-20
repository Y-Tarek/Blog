
from django.db import models
from django.utils.text import slugify

class TimeStampModel(models.Model):
    """
    Abstract model with timestamp fields (created_at and updated_at).
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Class meta for TimeStampModel model."""

        abstract = True

class TimeStampedWithNamesModel(TimeStampModel):
    """ 
     Abstract model inherits from TimeStampModel and have the (name,slug) fields.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        """Class meta for TimeStampedWithNamesModel model."""

        abstract = True

    def __str__(self):
        model_name = self._meta.verbose_name.title()
        return f"{model_name}: {self.name}"