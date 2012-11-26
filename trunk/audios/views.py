# Create your views here.

import os, string
import datetime
from django.utils import timezone 

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

from django.core.files import File
from django.core.files.base import ContentFile

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from audios.models import Speaker, Audio

def _generate_random_string(length, stringset=string.ascii_letters):
    return ''.join([stringset[i%len(stringset)] \
        for i in [ord(x) for x in os.urandom(length)]])

def record(request):
    if request.method == 'GET':

        request.session['session-id'] = _generate_random_string(20)

        t = loader.get_template('basic.html')
        return HttpResponse(t.render(Context({})))

@csrf_exempt
def wami_handler(request):

    if request.method == 'GET':

        filename = request.session['session-id'] 
        f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'r')
        myfile = File(f)
        data = myfile.read()
        myfile.close()
        f.close()

        Ctype = 'audio/x-wav'        
        response = HttpResponse(data, content_type=Ctype)

        return response
    
    if request.method == 'POST':

        filename = request.session['session-id'] 
        f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'wb')
        myfile = File(f) 
        myfile.write(request.body)
        myfile.close()
        f.close()

        return HttpResponse('Ok')
	#yield HttpResponse('Ok')

#def list(request):
#    if request.method == 'GET':
#        return HttpResponse("Hello, world.")

#=================================================================

def start(request):
    if request.method == 'GET':
        request.session['session-id'] = _generate_random_string(20)

        t = loader.get_template('start.html')
        return HttpResponse(t.render(Context({})))

@csrf_exempt
def add_speaker(request):    
    if request.method == 'POST':

        # save the speaker
        now = timezone.now()
        accent = request.POST['accent']
        location = request.POST['location']

        session = request.session['session-id']
        speaker = Speaker(date= now, location= location, accent= accent, session= session)
        speaker.save()

        tests = Context({ 
            '1':'fernet', 
            '2':'camioneta', 
            '3':'El cuarteto es lo mejor que hay!'
            #'tests_list' :
            #    {
            #        '1':'fernet', 
            #        '2':'camioneta', 
            #        '3':'El cuarteto es lo mejor que hay!'
            #    }
        })
        
        return HttpResponseRedirect("/audios/record_tests/")

def record_tests(request):
    if request.method == 'GET':
        tests_list = Context({ '1':'fernet', '2':'camioneta', '3':'El cuarteto es lo mejor que hay!',})
        t = loader.get_template('record_tests.html')
        return HttpResponse(t.render(tests_list))

@csrf_exempt
def wami_handler2(request):

    if request.method == 'GET':

        filename = request.session['session-id']+"_"+request.GET['name_test']
        f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'r')
        myfile = File(f)
        data = myfile.read()
        myfile.close()
        f.close()

        Ctype = 'audio/x-wav'        
        response = HttpResponse(data, content_type=Ctype)

        return response
    
    if request.method == 'POST':

        filename = request.session['session-id']+"_"+request.GET['name_test']
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
        speaker = Speaker.objects.filter(session= request.session['session-id'])[0]

        # Grabar los audios con usando el modelo        
        for name_test in ['test1', 'test2', 'test3']:
            filename = request.session['session-id']+"_"+name_test
            f = open(os.path.join(settings.MEDIA_ROOT, filename+'.wav'), 'r')
            myfile = File(f)
            data = myfile.read()
            myfile.close()
            f.close()
                        
            # grabar audios
            audio = Audio(text=name_test, speaker=speaker)

            #f = open(os.path.join(settings.MEDIA_ROOT+'confirmados/', filename+'.wav'), 'wb')
            #myfile = File(f) 
            #myfile.write(data)

            file_content = ContentFile(data)
            audio.audio.save(filename+'.wav', file_content) 

            #myfile.close()
            #f.close()

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
                