from django.db import models

# Create your models here.
class Speaker(models.Model):
    date = models.DateTimeField(auto_now=True)
    location = models.TextField()
    accent = models.TextField()
    session = models.TextField()
    birthDate = models.DateTimeField()
    age = models.IntegerField(default=0)
    finish = models.BooleanField(default=False)
    #no olvidarse genero

class Audio(models.Model):
    text = models.TextField()
    audio = models.FileField(upload_to='audios')
    speaker = models.ForeignKey(Speaker)
