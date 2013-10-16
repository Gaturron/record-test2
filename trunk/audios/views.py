#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create your views here.

import csv, os, zipfile, StringIO, glob, string, ast
from datetime import datetime
from django.utils import timezone 

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from audios.models import Speaker, Audio, LogSpeaker, LogVolume
from experiments.models import Word, Phrase, Picture, trace

def _generate_random_string(length, stringset=string.ascii_letters):
    return ''.join([stringset[i%len(stringset)] \
        for i in [ord(x) for x in os.urandom(length)]])

#=================================================================

def start(request):
    if request.method == 'GET':

        request.session['session-rmz'] = _generate_random_string(20)
        # numero generado al azar para identificar a un hablante nuevo

        t = loader.get_template('start.html')
        return HttpResponse(t.render(Context({})))

@csrf_exempt
def add_speaker(request):    
    if request.method == 'POST':

        # save the speaker
        now = timezone.now()
        location = request.POST['location']
        session = request.session['session-rmz']

        sex = request.POST['sex']
        birthPlace = request.POST['birthPlace']
        livePlace = request.POST['livePlace']
        birthDate = datetime.strptime(str(request.POST['birthDate']), "%m-%Y")

        # age calculator
        dt = now - birthDate
        age = dt.days / 365
        
        speaker = Speaker(date= now, location= location, session= session, sex= sex, birthPlace= birthPlace, livePlace= livePlace, birthDate=birthDate, age= age)
        speaker.save()

        return HttpResponseRedirect("/audios/record_tests1/")

def record_tests1(request):
    if request.method == 'GET':

        try:
            #Chequear que es un usuario que recien lleno los datos
            if 'session-rmz' in request.session:
                session = request.session['session-rmz']
                speaker = Speaker.objects.get(session=session)

                #Agarro los experimentos que se guardaron
                path = trace.objects.filter(used= False)[0]
                trace_list = ast.literal_eval(path.phrases)
                path.used = True
                path.save()

                experiments = []
                for ti in trace_list:
                    word = Word.objects.get(id= ti)
                    experiments.append(word)

                t = loader.get_template('record_tests1.html')
                c = Context({ 
                    'speaker_id' : speaker.id,
                    'word_list' : experiments 
                })

                del request.session['session-rmz']
                request.session['speaker-id'] = speaker.id 
                request.session['speaker-accent'] = speaker.livePlace
                #speaker.livePlace == speaker-accent

                return HttpResponse(t.render(c))

            else:
                return HttpResponseRedirect("/audios/start/")

        except ObjectDoesNotExist:
            return HttpResponseRedirect("/audios/start/")

@csrf_exempt
def wami_handler2(request):

    if request.method == 'GET':
        #play

        filename = str(request.session['speaker-accent'])+"_u"+str(request.session['speaker-id'])+"_t"+request.GET['name_test']+"_a"+request.GET['attempts']
        f = open(os.path.join(settings.MEDIA_ROOT, "audios/"+filename+'.wav'), 'r')
        myfile = File(f)
        data = myfile.read()
        myfile.close()
        f.close()

        Ctype = 'audio/x-wav'        
        response = HttpResponse(data, content_type=Ctype)

        return response
    
    if request.method == 'POST':
        #record
        
        speakerId = str(request.session['speaker-id'])
        speaker = Speaker.objects.get(id= speakerId)

        wordId = request.GET['name_test']
        word = Word.objects.get(id= wordId)

        attempt = str(request.GET['attempts'])

        filename = str(request.session['speaker-accent'])+"_u"+speakerId+"_t"+wordId+"_a"+attempt
        print "Archivo de audio a grabar: "+filename

        audio = Audio(speaker= speaker, word= word, attempt=attempt, filename= filename)
        audio.save()

        f = open(os.path.join(settings.MEDIA_ROOT, "audios/"+filename+'.wav'), 'wb')
        myfile = File(f) 
        myfile.write(request.body)
        myfile.close()
        f.close()

        return HttpResponse('Ok')


def end(request):
    if request.method == 'GET':
        t = loader.get_template('end.html')
        return HttpResponse(t.render(Context({ })))

#======================================================================
# Get info

def audio_editor(request, id):
    if request.method == 'GET':
        audio = Audio.objects.get(id= id)
        t = loader.get_template('audio_editor.html')
        c = Context({
            'audio': audio,
            'labels': audio.labels.all()
        })
        return HttpResponse(t.render(c))

def audio_url(request, id):
    if request.method == 'GET':
        audio = Audio.objects.get(id= id)
        filename = audio.filename
        
        f = open(os.path.join(settings.MEDIA_ROOT, "audios/"+filename+'.wav'), 'r')
        myfile = File(f)
        data = myfile.read()
        
        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s.wav' % filename

        return response

def audioList(request):
    if request.method == 'GET':
        speakers_list = Speaker.objects.all()[:5]
        audios_list = Audio.objects.all()
        t = loader.get_template('list.html')
        c = Context({
            'speakers_list': speakers_list,
            'audios_list': audios_list
        })
        return HttpResponse(t.render(c))


def speakerList(request):
    if request.method == 'GET':
        speakerList = Speaker.objects.all()[:]
        t = loader.get_template('speakerList.html')
        c = Context({
            'speakerList': speakerList
        })
        return HttpResponse(t.render(c))

#======================================================================
# Logging

@csrf_exempt
def writeLog(request):        
    if request.method == 'POST':

        speakerId = int(request.POST['speakerId'])
        action = request.POST['action']
        wordId = int(request.POST['wordId'])
        attempt = int(request.POST['attempt'])
        log = LogSpeaker(speakerId= speakerId, action= action, wordId= wordId, attempt= attempt)
        log.save()

        return HttpResponse('Ok')

@csrf_exempt
def writeLogVolume(request):
    if request.method == 'POST':

        speakerId = int(request.POST['speakerId'])
        action = request.POST['action']
        wordId = int(request.POST['wordId'])
        attempt = int(request.POST['attempt'])
        volumen = (str(request.POST['volumen'])).split(",")

        volumen_parts = []
        while volumen:
            volumen_parts.append(volumen[:800])
            volumen = volumen[800:]

        speaker = Speaker.objects.get(id= speakerId)
        word = Word.objects.get(id= wordId)
        audio = Audio.objects.get(speaker= speaker, word= word, attempt= attempt)
        if audio:
            audioId = audio.id
        else:
            audioId = 0

        part = 1
        for i in volumen_parts:
            logVolume = LogVolume(audioId= audioId, part= part, volume= i)
            logVolume.save()
            part = part + 1

        log = LogSpeaker(speakerId= speakerId, action= action, wordId= wordId, attempt= attempt)
        log.save()

        return HttpResponse('Ok')        

# No usado por ahora
def logSpeakerList(request):
    if request.method == 'GET':
        logSpeakerList = LogSpeaker.objects.all()[:]
        t = loader.get_template('logSpeakerList.html')
        c = Context({
            'logSpeakerList': logSpeakerList
        })
        return HttpResponse(t.render(c))

def logVolumeList(request):
    if request.method == 'GET':
        logVolumeList = LogVolume.objects.all()[:]
        t = loader.get_template('logVolumeList.html')
        c = Context({
            'logVolumeList': logVolumeList
        })
        return HttpResponse(t.render(c))

#======================================================================
# Backup
def speakersToCSV(request):
    if request.method == 'GET':
        speakers = Speaker.objects.all()

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="backup-speakers'+str(timezone.now())+'.csv"'

        writer = csv.writer(response)

        writer.writerow(["id", "date", "location", "session", "sex", "birthPlace", "livePlace", "birthDate", "age"])
        for speaker in speakers:
            writer.writerow([str(speaker.id), str(speaker.date), str(speaker.location), str(speaker.session), str(speaker.sex), str(speaker.birthPlace), str(speaker.livePlace), str(speaker.birthDate), str(speaker.age)])

        return response

def logSpeakerToCSV(request):
    if request.method == 'GET':
        logSpeakers = LogSpeaker.objects.all()

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="backup-logSpeakers'+str(timezone.now())+'.csv"'

        writer = csv.writer(response)

        writer.writerow(["id", "speakerId", "action", "wordId", "attempt", "date"])
        for logSpeaker in logSpeakers:
            writer.writerow([str(logSpeaker.id), str(logSpeaker.speakerId), str((logSpeaker.action).encode('ascii', 'ignore')), str(logSpeaker.wordId), str(logSpeaker.attempt), str(logSpeaker.date)])

        return response

def logVolumeToCSV(request):
    if request.method == 'GET':
        logVolumes = LogVolume.objects.all()

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="backup-logVolumes'+str(timezone.now())+'.csv"'

        writer = csv.writer(response)

        writer.writerow(["id", "audioId", "volume", "part"])
        for logVolume in logVolumes:
            writer.writerow([str(logVolume.id), str(logVolume.audioId), str(logVolume.volume), str(logVolume.part)])

        return response

def zipAudios(request):

    if request.method == 'GET':

        o = StringIO.StringIO()
        zf = zipfile.ZipFile(o, mode='w')
        
        for audio in glob.glob(settings.MEDIA_ROOT+'/audios/*.wav'):
            zf.write(str(audio), os.path.basename(str(audio)))
        
        zf.close()
        o.seek(0)
        response = HttpResponse(o.read())
        o.close()
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="backup-audios'+str(timezone.now())+'.zip"'
        return response