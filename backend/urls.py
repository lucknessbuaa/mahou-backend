from django.conf.urls import patterns, include, url
#import views


urlpatterns = patterns('backend.magician_views',
    url(r'^magician$','magician'),
    url(r'^magician/add$','add_magician'),
    url(r'^magician/delete$','delete_magician'),
    url(r'^magician/(?P<id>\d+)$','edit_magician'),
)

urlpatterns = urlpatterns + patterns('backend.show_views',
    url(r'^show$','show'),
    url(r'^show/add$','add_show'),
    url(r'^show/delete$','delete_show'),
    url(r'^show/requireMag$','requireMag'),
    url(r'^show/(?P<id>\d+)$','edit_show'),
)

urlpatterns = urlpatterns + patterns('backend.new_views',
    url(r'^new$','new'),
)