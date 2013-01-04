from django.conf.urls import patterns, include, url

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
    url(r'^audios/record_tests/$',   'audios.views.record_tests'), 
    url(r'^audios/wamihandler2/$',   'audios.views.wami_handler2'),  
    url(r'^audios/confirm_audios/$', 'audios.views.confirm_audios'), 

    url(r'^audios/audio_url/(?P<id>\d+)/$',      'audios.views.audio_url', name="audio_url"), 
    url(r'^audios/list/$',           'audios.views.list'),

    #================================================================
    # Words
    url(r'^experiments/words/list/$',               'experiments.views.wordsList'),
    url(r'^experiments/words/add/$',                'experiments.views.addWord'),
    url(r'^experiments/words/edit/(?P<id>\d+)/$',   'experiments.views.editWord', name="editWord"), 
    url(r'^experiments/words/delete/(?P<id>\d+)/$', 'experiments.views.deleteWord', name="deleteWord"), 
    url(r'^experiments/words/enable/(?P<id>\d+)/$', 'experiments.views.enableWord', name="enableWord"), 
 
    # Pictures
    url(r'^experiments/pictures/list/$',               'experiments.views.picturesList'),
    url(r'^experiments/pictures/add/$',                'experiments.views.addPicture'),
    url(r'^experiments/pictures/show/(?P<id>\d+)/$',   'experiments.views.showPicture', name="showPicture"),
    url(r'^experiments/pictures/edit/(?P<id>\d+)/$',   'experiments.views.editPicture', name="editPicture"), 
    url(r'^experiments/pictures/delete/(?P<id>\d+)/$', 'experiments.views.deletePicture', name="deletePicture"), 
    url(r'^experiments/pictures/enable/(?P<id>\d+)/$', 'experiments.views.enablePicture', name="enablePicture"), 
)
