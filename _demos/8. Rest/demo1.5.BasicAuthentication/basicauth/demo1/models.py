from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        permissions = [
            ("rate_movie", "Can rate the movie"),
            ("close_movie", "Can remove a movie by setting its status as closed"),
        ]

