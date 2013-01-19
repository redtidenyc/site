from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from rt_www.photogallery.models import Video
from django.views.generic.list_detail import object_list
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import cElementTree as ET
import cStringIO as String

#videos_info_dict = { 
#    'queryset':Video.objects.all(),
#    'template_name':'photogallery/video.html'
#}

def videos( request ): 
# *args, **kwargs):
    # try:
    #    kwargs['extra_context'] = { 'object':Video.objects.latest('date_uploaded') }
    #except:
    #    pass
    
    video_list = Video.objects.all() # object_list(*args, **kwargs)
    paginator = Paginator(video_list, 12) # Show 12 contacts per page

    page = request.GET.get('page',1)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        videos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)
    
    return render_to_response('photogallery/video.html', {"videos": videos})
    # return video_list

def playlist(request):
    root = ET.Element('playlist') 
    resp = ET.ElementTree(root)
    tlist = ET.SubElement(root, 'trackList')
    for v in Video.objects.all():
        track = ET.SubElement(tlist, 'track')
        title = ET.SubElement(track, 'title')
        location = ET.SubElement(track, 'location')
        image = ET.SubElement(track, 'image')
        location.text = v.get_video()
        image.text = v.get_thumb()
        title = str(v)
    respobj = HttpResponse('', mimetype='text/xml')
    resp.write(respobj, encoding='utf-8')
    return respobj
