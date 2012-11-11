from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^(\d+)/$', 'forum.views.forum'),
    url(r'^(\d+)/new_thread/$', 'forum.views.new_thread'),
    url(r'^thread/(?P<pk>\d+)/reply/$', 'forum.views.reply'),
    url(r'^thread/(?P<pk>\d+)/$', 'forum.views.thread'),
    url(r'', 'forum.views.main'),
)