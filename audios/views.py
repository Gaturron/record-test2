# -*- coding: utf-8 -*-

# Create your views here.

import os, string
import datetime
from django.utils import timezone 

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from audios.models import Speaker, Audio
from experiments.models import Word, Phrase, Picture

def _generate_random_string(length, stringset=string.ascii_letters):
    return ''.join([stringset[i%len(stringset)] \
        for i in [ord(x) for x in os.urandom(length)]])

# def record(request):
#     if request.method == 'GET':

#         request.session['session-id'] = _generate_random_string(20)

#         t = loader.get_template('basic.html')
#         return HttpResponse(t.render(Context({})))

# @csrf_exempt
# def wami_handler(request):

#     if request.method == 'GET':

#         filename = request.session['session-id'] 
#         f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'r')
#         myfile = File(f)
#         data = myfile.read()
#         myfile.close()
#         f.close()

#         Ctype = 'audio/x-wav'        
#         response = HttpResponse(data, content_type=Ctype)

#         return response
    
#     if request.method == 'POST':

#         filename = request.session['session-id'] 
#         f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'wb')
#         myfile = File(f) 
#         myfile.write(request.body)
#         myfile.close()
#         f.close()

#        return HttpResponse('Ok')

#def list(request):
#    if request.method == 'GET':
#        return HttpResponse("Hello, world.")

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
        accent = request.POST['accent']
        location = request.POST['location']
        session = request.session['session-rmz']
 
        #TODO: Arreglar birthdate y demas datos erroneos
        speaker = Speaker(birthDate=now, date= now, location= location, accent= accent, session= session)
        speaker.save()

        return HttpResponseRedirect("/audios/record_tests1/")

def record_tests(request):
    if request.method == 'GET':

        try:
            #Chequear que es un usuario que recien lleno los datos
            if 'session-rmz' in request.session:
                session = request.session['session-rmz']
                speaker = Speaker.objects.get(session=session, finish=False)

                #Agarro los experimentos que se guardaron
                word_list = Word.objects.all()[:]
                phrase_list = Phrase.objects.all()[:]
                pictures_list = Picture.objects.all()[:]

                t = loader.get_template('record_tests.html')
                c = Context({ 
                    'word_list' : word_list,
                    'phrase_list' : phrase_list,
                    'pictures_list': pictures_list 
                })

                del request.session['session-rmz']
                request.session['speaker-id'] = speaker.id 

                return HttpResponse(t.render(c))

            else:
                return HttpResponseRedirect("/audios/start/")

        except ObjectDoesNotExist:
            return HttpResponseRedirect("/audios/start/")

def record_tests1(request):
    if request.method == 'GET':

        try:
            #Chequear que es un usuario que recien lleno los datos
            if 'session-rmz' in request.session:
                session = request.session['session-rmz']
                speaker = Speaker.objects.get(session=session, finish=False)

                #Agarro los experimentos que se guardaron
                word_list = Word.objects.all()[:]
                phrase_list = Phrase.objects.all()[:]
                pictures_list = Picture.objects.all()[:]

                t = loader.get_template('record_tests1.html')
                c = Context({ 
                    'word_list' : word_list,
                    'phrase_list' : phrase_list,
                    'pictures_list': pictures_list 
                })

                del request.session['session-rmz']
                request.session['speaker-id'] = speaker.id 

                return HttpResponse(t.render(c))

            else:
                return HttpResponseRedirect("/audios/start/")

        except ObjectDoesNotExist:
            return HttpResponseRedirect("/audios/start/")

@csrf_exempt
def wami_handler2(request):

    if request.method == 'GET':

        filename = "u"+str(request.session['speaker-id'])+"_"+request.GET['name_test']
        f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'r')
        myfile = File(f)
        data = myfile.read()
        myfile.close()
        f.close()

        Ctype = 'audio/x-wav'        
        response = HttpResponse(data, content_type=Ctype)

        return response
    
    if request.method == 'POST':

        filename = "u"+str(request.session['speaker-id'])+"_"+request.GET['name_test']
        f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'wb')
        myfile = File(f) 
        myfile.write(request.body)
        myfile.close()
        f.close()

        return HttpResponse('Ok')

@csrf_exempt
def confirm_audios(request):
    if request.method == 'POST':

        # sacar speaker id
        speaker = Speaker.objects.get(id= request.session['speaker-id'])

        # Grabar los audios con usando el modelo  
        word_list = Word.objects.all()[:]
        phrase_list = Phrase.objects.all()[:]
        pictures_list = Picture.objects.all()[:]

        exp_list = []

        for test in word_list:
            exp_list.append({'type': 'w', 'id': str(test.id)})
        for test in phrase_list:
            exp_list.append({'type': 'ph', 'id': str(test.id)})
        for test in pictures_list:
            exp_list.append({'type': 'pic', 'id': str(test.id)})
        
        for exp in exp_list:
            filename = "u"+str(speaker.id)+"_"+"test-"+exp['type']+exp['id']
            
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, filename+'.wav')):
                
                #grabo el audio definitivo
                f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'r')
                myfile = File(f)
                data = myfile.read()
                myfile.close()
                f.close()
                            
                # grabar audios
                audio = Audio(text=filename, speaker=speaker)

                file_content = ContentFile(data)
                audio.audio.save(filename+'.wav', file_content) 

                #borro el archivo temporal
                os.remove(os.path.join(settings.MEDIA_ROOT, filename+'.wav'))

                #guardo que ese experimento se hizo una vez
                if(exp['type'] == 'w'):
                    word = Word.objects.get(id=exp['id'])
                    word.amount += 1
                    word.save()

                if(exp['type'] == 'ph'):
                    phrase = Phrase.objects.get(id=exp['id'])
                    phrase.amount += 1
                    phrase.save()

                if(exp['type'] == 'pic'):
                    picture = Picture.objects.get(id=exp['id'])
                    picture.amount += 1
                    picture.save()

        speaker.finish = True
        speaker.save()

        return HttpResponse("Gracias por colaborar!")

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
                