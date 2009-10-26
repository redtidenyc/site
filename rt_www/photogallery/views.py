from django.http import HttpResponse
from rt_www.photogallery.models import Video
from django.views.generic.list_detail import object_list
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import cElementTree as ET
import cStringIO as String

def videos(*args, **kwargs):
    try:
        kwargs['extra_context'] = { 'object':Video.objects.latest('date_uploaded') }
    except:
        pass
    return object_list(*args, **kwargs)

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
