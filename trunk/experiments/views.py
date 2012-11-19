# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from experiments.models import Word, Phrase, Picture
from experiments.forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt

#======================================================================
# Experimentos de palabras

def wordsList(request):
    if request.method == 'GET':
        word_list = Word.objects.all()[:]
        t = loader.get_template('wordsList.html')
        c = Context({
            'word_list': word_list
        })
        return HttpResponse(t.render(c))

@csrf_exempt
def addWord(request):
    if request.method == 'GET':
        t = loader.get_template('addWord.html')
        return HttpResponse(t.render(Context()))

    if request.method == 'POST':
        enabled = False
        if "enabled" in request.POST.keys():
            enabled = request.POST['enabled']
            
        text = request.POST['text']
        description = request.POST['description']
        
        if "id" in request.POST.keys():
            w = Word.objects.get(id=request.POST['id'])
            w.enabled = enabled
            w.text = text
            w.description = description
        else:
            w = Word(enabled= enabled, text= text, description= description)
        w.save()

        return HttpResponseRedirect("/experiments/words/list/")

@csrf_exempt
def editWord(request, id):
    if request.method == 'GET':

        word = Word.objects.get(id=id)

        t = loader.get_template('addWord.html')
        c = Context({
            'id': id,
            'word': word
        })
        return HttpResponse(t.render(c))

@csrf_exempt
def deleteWord(request, id):
    if request.method == 'POST':
        word = Word.objects.get(id=id)
        word.delete()
        return HttpResponseRedirect("/experiments/words/list/")

@csrf_exempt
def enableWord(request, id):
    if request.method == 'POST':
        word = Word.objects.get(id=id)
        word.enabled = not word.enabled
        word.save()
        return HttpResponseRedirect("/experiments/words/list/")
        
#======================================================================
# Experimentos de Imagenes

def picturesList(request):
    if request.method == 'GET':
        pictures_list = Picture.objects.all()[:]
        t = loader.get_template('picturesList.html')
        c = Context({
            'pictures_list': pictures_list
        })
        return HttpResponse(t.render(c))

@csrf_exempt
def addPicture(request):
    if request.method == 'GET':
        t = loader.get_template('addPicture.html')
        form = UploadFileForm()
        return HttpResponse(t.render(Context({'form': form})))

    if request.method == 'POST':
        enabled = False
        if "enabled" in request.POST.keys():
            enabled = request.POST['enabled']
            
        description = request.POST['description']
        
        form = UploadFileForm(request.POST, request.FILES)
        image = request.FILES['uploadField']

        if "id" in request.POST.keys():
            p = Picture.objects.get(id=request.POST['id'])
            
            p.enabled = enabled
            p.description = description
            p.image = image 
            p.save()
        else:
            p = Picture(enabled= enabled, image= image, description= description)
            p.save()

        return HttpResponseRedirect("/experiments/pictures/list/")

@csrf_exempt
def editPicture(request, id):
    if request.method == 'GET':

        picture = Picture.objects.get(id=id)

        t = loader.get_template('addWord.html')
        c = Context({
            'id': id,
            'picture': picture
        })
        return HttpResponse(t.render(c))

@csrf_exempt
def deletePicture(request, id):
    if request.method == 'POST':
        picture = Picture.objects.get(id=id)
        picture.delete()
        return HttpResponseRedirect("/experiments/pictures/list/")

@csrf_exempt
def enablePicture(request, id):
    if request.method == 'POST':
        picture = Picture.objects.get(id=id)
        picture.enabled = not picture.enabled
        picture.save()
        return HttpResponseRedirect("/experiments/pictures/list/")

