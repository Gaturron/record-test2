from django.db import models

# Create your models here.
class Word(models.Model):
    enabled = models.BooleanField(default=True)
    text = models.TextField()
    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField(default=0)

class Phrase(models.Model):
    enabled = models.BooleanField(default=True)
    text = models.TextField()
    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField(default=0)

class Picture(models.Model):
    enabled = models.BooleanField(default=True)
    image = models.FileField(upload_to='imagenesExperimentos')
    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField(default=0)