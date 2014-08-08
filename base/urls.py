from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from mahou import settings
from tastypie.api import Api
import base.views

urlpatterns = patterns('',
    url(r'^/?$', 'base.views.welcome'),
    url(r'^login$', 'base.views.login'),
    url(r'^login.json$','base.views.loginByJSON'),
    url(r'^logout$','base.views.logout'),
    url(r'^welcome$','base.views.welcome'),

    url(r'^ajax-upload/', include('ajax_upload.urls')),

    url(r'^backend/', include('backend.urls')),
    #url(r'^API/input','backend.views.ajax_add'),
    #url(r'^API/',include(v.urls)) 

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
