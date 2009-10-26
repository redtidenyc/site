from django.conf.urls.defaults import *
from django.conf import settings
from rt_www.photogallery.models import Video

videos_info_dict = { 
    'queryset':Video.objects.all(),
    'template_name':'photogallery/video.html'
}


urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', { 'template':'photogallery/index.html' }),
    (r'^videos', 'rt_www.photogallery.views.videos', videos_info_dict),    
    (r'^playlist', 'rt_www.photogallery.views.playlist'),
)
