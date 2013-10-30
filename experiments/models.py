from django.db import models

# Create your models here.
class Word(models.Model):
    enabled = models.BooleanField(default=True)
    text = models.TextField()
    description = models.TextField(blank=True, null=True)

# not used
class Phrase(models.Model):
    enabled = models.BooleanField(default=True)
    text = models.TextField()
    description = models.TextField(blank=True, null=True)

# not used
class Picture(models.Model):
    enabled = models.BooleanField(default=True)
    image = models.FileField(upload_to='imagenesExperimentos')
    description = models.TextField(blank=True, null=True)

class trace(models.Model):
    phrases = models.CommaSeparatedIntegerField(max_length=200)
    used = models.BooleanField(default=False)
    