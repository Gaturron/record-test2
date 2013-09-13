from django.db import models
from experiments.models import Word

# Create your models here.
class Speaker(models.Model):
    #calculados
    date = models.DateTimeField(auto_now=True)
    location = models.TextField()
    session = models.TextField()

    #preguntados del form
    sex = models.TextField()
    birthPlace = models.TextField()
    livePlace = models.TextField()
    birthDate = models.DateTimeField()

    #que se pueden calcular
    age = models.IntegerField(default=0)
    
class Audio(models.Model):
    speaker = models.ForeignKey(Speaker)
    word = models.ForeignKey(Word)
    #opcion B
    #ItemId = models.IntegerField(default=0)
    attempt = models.IntegerField(default=0)
    filename = models.TextField()

class LogSpeaker(models.Model):
    speakerId = models.IntegerField()
    action = models.TextField()
    ItemId = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

class LogVolume(models.Model):
    LogSpeaker = models.ForeignKey(LogSpeaker)
    volume = models.CommaSeparatedIntegerField(max_length=800)
    part = models.IntegerField()