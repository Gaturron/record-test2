from django.conf.urls import patterns, include, url
from django.views.static import * 
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

    #prueba
    #url(r'^audios/record/$',         'audios.views.record'),
    #url(r'^audios/wamihandler/$',    'audios.views.wami_handler'),

    url(r'^audios/start/$',          'audios.views.start', name="home"),
    url(r'^audios/add_speaker/$',    'audios.views.add_speaker'), 
    #url(r'^audios/record_tests/$',   'audios.views.record_tests'), 
    url(r'^audios/record_tests1/$',   'audios.views.record_tests1'), 
    url(r'^audios/wamihandler2/$',   'audios.views.wami_handler2'),  
    url(r'^audios/confirm_audios/$', 'audios.views.confirm_audios'), 
    url(r'^audios/writeLog/$',       'audios.views.writeLog'),
    url(r'^audios/writeLogVolume/$',       'audios.views.writeLogVolume'),

    url(r'^audios/audio_url/(?P<id>\d+)/$',      'audios.views.audio_url', name="audio_url"), 
    url(r'^audios/list/$',           'audios.views.list'),

    url(r'^audios/end/$',            'audios.views.end'),

    #================================================================
    # Backup
    
    url(r'^speakers/backup/$',       'audios.views.speakersToCSV'),
    url(r'^speakers/zip_audios/$',   'audios.views.zipAudios'),    

    #================================================================
    #Admin
    url(r'^experiments/admin/$',                   'experiments.views.admin'),
    url(r'^experiments/populate/$',                'experiments.views.populateDB'),

    # Words
    url(r'^experiments/words/list/$',               'experiments.views.wordsList'),
    url(r'^experiments/words/add/$',                'experiments.views.addWord'),
    url(r'^experiments/words/showExp/(?P<id>\d+)/$',   'experiments.views.showWordExp', name="showWordExp"),
    url(r'^experiments/words/edit/(?P<id>\d+)/$',   'experiments.views.editWord', name="editWord"), 
    url(r'^experiments/words/delete/(?P<id>\d+)/$', 'experiments.views.deleteWord', name="deleteWord"), 
    url(r'^experiments/words/enable/(?P<id>\d+)/$', 'experiments.views.enableWord', name="enableWord"), 
    url(r'^experiments/arrayIdWords/$',             'experiments.views.arrayIdWords'), 
 
    # Pictures
    url(r'^experiments/pictures/list/$',               'experiments.views.picturesList'),
    url(r'^experiments/pictures/add/$',                'experiments.views.addPicture'),
    url(r'^experiments/pictures/showExp/(?P<id>\d+)/$',   'experiments.views.showPicExp', name="showPicExp"),    
    url(r'^experiments/pictures/show/(?P<id>\d+)/$',   'experiments.views.showPicture', name="showPicture"),
    url(r'^experiments/pictures/edit/(?P<id>\d+)/$',   'experiments.views.editPicture', name="editPicture"), 
    url(r'^experiments/pictures/delete/(?P<id>\d+)/$', 'experiments.views.deletePicture', name="deletePicture"), 
    url(r'^experiments/pictures/enable/(?P<id>\d+)/$', 'experiments.views.enablePicture', name="enablePicture"), 
    url(r'^experiments/arrayIdPics/$',                 'experiments.views.arrayIdPics')
)

handler404 = views.error404
handler500 = views.error404