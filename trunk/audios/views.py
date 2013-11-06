#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create your views here.

import csv, os, zipfile, tarfile, StringIO, glob, string, ast
from datetime import datetime
from django.utils import timezone 

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from audios.models import Speaker, Audio, LogSpeaker, LogVolume, audioLabel
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

@csrf_exempt
def audio_editor(request, id):
    if request.method == 'GET':
        audio = Audio.objects.get(id= id)
        t = loader.get_template('audio_editor.html')
        c = Context({
            'audio': audio,
            'audio_labels': audio.labels.all(),
            'labels': audioLabel.objects.all()
        })
        return HttpResponse(t.render(c))

    if request.method == 'POST':
        audio = Audio.objects.get(id= id)
        id_labels = request.POST.getlist('label')
        audio.labels.clear()

        for id_label in id_labels:
            label = audioLabel.objects.get(id= id_label)
            audio.labels.add(label)
        audio.save()

        return HttpResponseRedirect("/admin/audioList/")

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
        speakers_list = Speaker.objects.all()
        audios_list = Audio.objects.order_by('filename')
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

def audiosToCSV(request):
    if request.method == 'GET':
        audios = Audio.objects.all()

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="backup-audios'+str(timezone.now())+'.csv"'

        writer = csv.writer(response)

        writer.writerow(["id", "speaker", "word", "attempt", "filename", "labels"])
        for audio in audios:
            writer.writerow([str(audio.id), str(audio.speaker.id), str(audio.word.id), str(audio.attempt), str(audio.filename), str(map(lambda l: l.name, audio.labels.all()))])

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

def zipAudios(request, filter):

    if request.method == 'GET':

        o = StringIO.StringIO()
        tar = tarfile.open(None, mode='w', fileobj=o)

        if(filter == 'conservado'):
            audios = Audio.objects.filter(labels__name='Conservar')
        elif(filter == 'saturado'):
            audios = Audio.objects.filter(labels__name='Sonido saturado')
        elif(filter == 'ruido'):
            audios = Audio.objects.filter(labels__name='Mucho ruido de fondo')
        elif(filter == 'problema'):
            audios = Audio.objects.filter(labels__name='Problema en el habla')
        elif(filter == 'total'):
            audios = Audio.objects.all()
        else: 
            audios = Audio.objects.all()

        for audio in audios:
            name = settings.MEDIA_ROOT+'/audios/'+audio.filename+'.wav'
            tar.add(str(name), os.path.basename(str(name)))
        
        tar.close()

        o.seek(0)
        response = HttpResponse(o.read())
        o.close()
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="backup-audios-'+filter+'-'+str(timezone.now())+'.tar"'
        return response

#======================================================================
#Estadisticas
def statistics(request):

    if request.method == 'GET':

        spBsas = Speaker.objects.filter(livePlace='bsas').count()
        spCba = Speaker.objects.filter(livePlace='cba').count()

        wordsCount = []

        phrasesXrules = { 
            1: [2],
            2: [2],
            3: [6],
            4: [2],
            5: [2,3],
            6: [2],
            7: [6],
            8: [2,3],
            9: [2],
            10 : [2],
            11 : [2],
            12 : [2],
            13 : [],
            14 : [],
            15 : [3],
            16 : [2, 6],
            17 : [],
            18 : [5],
            19 : [2],
            20 : [5],
            21 : [6],
            22 : [2,4],
            23 : [3],
            24 : [2,6],
            25 : [],
            26 : [2,4],
            27 : [4],
            28 : [2,4],
            29 : [],
            30 : [2],
            31 : [5],
            32 : [5],
            33 : [2,5],
            34 : [5],
            35 : [4,5],
            36 : [2,4],
            40 : [1],
            41 : [1],
            42 : [1],
            43 : [1, 5, 6],
            44 : [1, 5, 6],
            45 : [1, 5, 6],
            46 : [1, 6],
            47 : [1, 6],
            48 : [1, 6]
        }

        #recorremos las frases y vemos como fueron completadas
        for word in Word.objects.all():
            count = Audio.objects.filter(word= word).count()
            wordsCount.append({ 'id': word.id, 'text': word.text, 'count': count, 'rules': phrasesXrules[word.id]})

        #contamos cuantas se completaron por cada regla
        rules = {}
        rules[1] = {'text': 'Localice la sílaba acentuada en la palabra y estirar la silaba anterior', 'count': 0}
        rules[2] = {'text': 'Aspiración y elisión de /s/', 'count': 0}
        rules[3] = {'text': 'La ‘s’ antes de la `c` o `t` suenan suaves', 'count': 0}
        rules[4] = {'text': 'La `c` antes de la `t` no se pronuncia', 'count': 0}
        rules[5] = {'text': 'La ‘y’ y ‘ll’ se pasa a ‘i’', 'count': 0}
        rules[6] = {'text': 'La ‘r’ no debe sonar. No debe vibrar', 'count': 0}

        for wordc in wordsCount:
            if wordc['count'] != 0:
                wordc_rules = wordc['rules']
                for r in wordc_rules:
                    rules[r]['count'] += wordc['count']

        traces = trace.objects.filter(used= False).count()

        t = loader.get_template('statistics.html')
        c = Context({
            'spBsas': spBsas,
            'spCba': spCba,
            'wordsCount': wordsCount,
            'rules': rules,
            'trace': traces
        })
        return HttpResponse(t.render(c))