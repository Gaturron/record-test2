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

    url(r'^audios/record/$',         'audios.views.record'),
    url(r'^audios/wamihandler/$',    'audios.views.wami_handler'),

    url(r'^audios/start/$',          'audios.views.start', name="home"),
    url(r'^audios/add_speaker/$',    'audios.views.add_speaker'), 
    url(r'^audios/record_tests/$',   'audios.views.record_tests'), 
    url(r'^audios/wamihandler2/$',   'audios.views.wami_handler2'),  
    url(r'^audios/confirm_audios/$', 'audios.views.confirm_audios'), 

    url(r'^audios/audio_url/(?P<id>\d+)/$',      'audios.views.audio_url', name="audio_url"), 
    url(r'^audios/list/$',           'audios.views.list'),

)
