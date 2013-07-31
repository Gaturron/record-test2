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

class LogSpeaker(models.Model):
    speakerId = models.IntegerField()
    action = models.TextField()
    ItemId = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

class LogVolume(models.Model):
    LogSpeaker = models.ForeignKey(LogSpeaker)
    volume = models.CommaSeparatedIntegerField(max_length=800)
    # Aca debemos guardar el vector de volumenes: max_length debe poner algo
    # setTimeout vamos a pasarle un valor por cuantos ms va a sensar
    # Sensamos a 50 ms => 20 muestras por segundo
    # 1 muestra son 2 caracteres + la coma + espacio = 4 caracteres
    # 80 caracteres por segundo 
    # suponemos que las grabaciones no van a superar los 10 segundos
    # => max_length = 20 * 4 * 10 = 800