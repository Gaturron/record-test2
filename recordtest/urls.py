from django.conf.urls import patterns, include, url
from django.views.static import * 
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls import handler404, handler500
from recordtest import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recordtest.views.home', name='home'),
    # url(r'^recordtest/', include('recordtest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #================================================================
    # Urls para los usuarios
    url(r'^$', RedirectView.as_view(url='http://habla.dc.uba.ar')),

    url(r'^audios/start/$',                 'audios.views.start', name="home"),
    url(r'^audios/add_speaker/$',           'audios.views.add_speaker'), 

    url(r'^audios/record_tests1/$',          'audios.views.record_tests1'), 
    url(r'^audios/wamihandler2/$',           'audios.views.wami_handler2'),  
    
    url(r'^audios/writeLog/$',               'audios.views.writeLog'),
    url(r'^audios/log/$',                    'audios.views.logSpeakerList'),
    
    url(r'^audios/writeLogVolume/$',         'audios.views.writeLogVolume'),
    url(r'^audios/logVolume/$',              'audios.views.logVolumeList'),

    url(r'^audios/end/$',                    'audios.views.end'),

    #================================================================
    # Get info

    url(r'^audios/speakerList/$',            'audios.views.speakerList'),
    url(r'^audios/audioList/$',              'audios.views.audioList'),
    url(r'^audios/audio_url/(?P<id>\d+)/$',  'audios.views.audio_url', name="audio_url"), 

    #================================================================
    # Backup
    
    url(r'^backup/speakers/$',      'audios.views.speakersToCSV'),
    url(r'^backup/logSpeakers/$',   'audios.views.logSpeakerToCSV'),
    url(r'^backup/logVolume/$',     'audios.views.logVolumeToCSV'),
    url(r'^backup/zip_audios/$',           'audios.views.zipAudios'),    

    #================================================================
    #Admin
    # solo usado para setear al principio los experimentos
    #url(r'^experiments/admin/$',                   'experiments.views.admin'),
    #url(r'^experiments/populate/$',                'experiments.views.populateDB'),

    # Words
    #url(r'^experiments/words/list/$',               'experiments.views.wordsList'),
    #url(r'^experiments/words/add/$',                'experiments.views.addWord'),
    #url(r'^experiments/words/showExp/(?P<id>\d+)/$',   'experiments.views.showWordExp', name="showWordExp"),
    #url(r'^experiments/words/edit/(?P<id>\d+)/$',   'experiments.views.editWord', name="editWord"), 
    #url(r'^experiments/words/delete/(?P<id>\d+)/$', 'experiments.views.deleteWord', name="deleteWord"), 
    #url(r'^experiments/words/enable/(?P<id>\d+)/$', 'experiments.views.enableWord', name="enableWord"), 
    #url(r'^experiments/arrayIdWords/$',             'experiments.views.arrayIdWords'), 
 
    # Pictures
    #url(r'^experiments/pictures/list/$',               'experiments.views.picturesList'),
    #url(r'^experiments/pictures/add/$',                'experiments.views.addPicture'),
    #url(r'^experiments/pictures/showExp/(?P<id>\d+)/$',   'experiments.views.showPicExp', name="showPicExp"),    
    #url(r'^experiments/pictures/show/(?P<id>\d+)/$',   'experiments.views.showPicture', name="showPicture"),
    #url(r'^experiments/pictures/edit/(?P<id>\d+)/$',   'experiments.views.editPicture', name="editPicture"), 
    #url(r'^experiments/pictures/delete/(?P<id>\d+)/$', 'experiments.views.deletePicture', name="deletePicture"), 
    #url(r'^experiments/pictures/enable/(?P<id>\d+)/$', 'experiments.views.enablePicture', name="enablePicture"), 
    #url(r'^experiments/arrayIdPics/$',                 'experiments.views.arrayIdPics')
)

handler404 = views.error404
handler500 = views.error404