from rt_www.video.models import Video

class Service:
    def get_thumb(self, pid):
        return Video.objects.get(pk=pid).get_thumb()
    def gallery_view(self, offset, limit):
        ret_val, offset, limit = {'count':Video.objects.count(), 'list':[]}, int(offset), int(limit)
        videos = Video.objects.all().order_by('-date')
        start, stop = offset, offset+limit
        if ret_val['count'] < stop:
            stop = ret_val['count']
        ret_val['list'] = [ { 'vid':v.id, 'thumburl':v.get_thumb(),
                'title':v.title }
                for v in videos ]
        if stop < len(ret_val['list']):
            ret_val['list'] = ret_val['list'][start:stop]
        else:
            ret_val['list'] = ret_val['list'][start:]
        return ret_val
        
service = Service()
