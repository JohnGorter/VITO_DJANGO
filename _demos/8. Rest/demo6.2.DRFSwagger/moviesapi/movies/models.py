from django.db import models

# Create your models here.
class Movie(models.Model):
    Title=models.CharField(max_length=20)
    