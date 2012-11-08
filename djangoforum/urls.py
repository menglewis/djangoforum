from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangoforum.views.home', name='home'),
    # url(r'^djangoforum/', include('djangoforum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^forum/(\d+)/$', 'forum.views.forum'),
    url(r'^thread/(\d+)/$', 'forum.views.thread'),
    url(r'^post/(new_thread|reply)/(\d+)/$', 'forums.views.post'),
    url(r'^reply/(\d+)/$', 'forums.views.reply'),
    url(r'^new_thread/(\d+)/$', 'forums.views.new_thread'),
    url(r'', 'forum.views.main'),
)
