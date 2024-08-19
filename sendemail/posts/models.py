from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"

    def __str__(self):
        return self.title

    