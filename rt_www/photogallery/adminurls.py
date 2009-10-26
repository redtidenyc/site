from django.conf.urls.defaults import *

urlpatterns = patterns('rt_www.photogallery.adminviews',
	(r'^$', 'index'),
	(r'^delete/(\d+)/$', 'delete_gallery'),
	(r'^(add)|(\d+)/$', 'change_gallery'),
)
