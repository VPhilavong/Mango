from django.db import models

# Create your models here.
class song_data(models.Model):
    artist = models.CharField(max_length=100)
    song = models.CharField(max_length=100)
 