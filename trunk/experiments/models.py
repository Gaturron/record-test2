from django.db import models

# Create your models here.
class Word(models.Model):
    enabled = models.BooleanField()
    text = models.TextField()
    description = models.TextField()

class Phrase(models.Model):
    enabled = models.BooleanField()
    text = models.TextField()
    description = models.TextField()

class Picture(models.Model):
    enabled = models.BooleanField()
    image = models.FileField(upload_to='imagenesExperimentos')
    description = models.TextField()