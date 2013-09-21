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

@csrf_exempt
def checkRecord(request):

    if request.method == 'GET':
        #check if the record finished correctly

        try:
            filename = str(request.session['speaker-accent'])+"_u"+str(request.session['speaker-id'])+"_t"+request.GET['name_test']+"_a"+request.GET['attempts']
            f = open(os.path.join(settings.MEDIA_ROOT, "audios/"+filename+'.wav'), 'r')
            myfile = File(f)
            data = myfile.read()
            myfile.close()
            f.close()
        except IOError as e:
            print "I/O Error({0}): {1}".format(e.errno, e.strerror)
            return HttpResponse("I/O Error: Try again")
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return HttpResponse("Unexpected Error: Try again")

        return HttpResponse("OK")

def audio_url(request, id):
    if request.method == 'GET':
        #audio = Audio.objects.get(id= request.GET['id'])
        audio = Audio.objects.get(id= id)
        audioFile = audio.audio

        filename = audioFile.name.split('/')[-1]
        response = HttpResponse(audioFile, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

def list(request):
    if request.method == 'GET':
        speakers_list = Speaker.objects.all()[:5]
        audios_list = Audio.objects.all()
        t = loader.get_template('list.html')
        c = Context({
            'speakers_list': speakers_list,
            'audios_list': audios_list
        })
        return HttpResponse(t.render(c))

def end(request):
    if request.method == 'GET':
        t = loader.get_template('end.html')
        return HttpResponse(t.render(Context({ })))

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

def speakerList(request):
    if request.method == 'GET':
        speakerList = Speaker.objects.all()[:]
        t = loader.get_template('speakerList.html')
        c = Context({
            'speakerList': speakerList
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

        for speaker in speakers:
            writer.writerow([str(speaker.id), str(speaker.date), str(speaker.location), str(speaker.accent), str(speaker.birthDate), str(speaker.age), str(speaker.finish), str(speaker.session)])

        return response

def zipAudios(request):

    if request.method == 'GET':

        o = StringIO.StringIO()
        zf = zipfile.ZipFile(o, mode='w')
        
        for audio in glob.glob(settings.MEDIA_ROOT+'/audios/*.wav'):
            i = open(str(audio), 'rb').read()
            zf.writestr(os.path.basename(str(audio)), i)
        
        zf.close()
        o.seek(0)
        response = HttpResponse(o.read())
        o.close()
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="backup-audios'+str(timezone.now())+'.zip"'
        return response