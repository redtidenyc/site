from photologue.models import Photo, Gallery
# from rt_www.photogallery.models import Photo, Gallery, PhotoPlace

class Service:
    def get_thumb(self, pid):
        return Photo.objects.get(pk=pid).get_thumb()
    def gallery_view(self, offset, limit):
        ret_val, offset, limit = {'count':Gallery.objects.count(), 'list':[]}, int(offset), int(limit)
        gallerys = Gallery.objects.all().order_by('-date')
        start, stop = offset, offset+limit
        if ret_val['count'] < stop:
            stop = ret_val['count']
        ret_val['list'] = [ { 'gid':g.id, 'thumburl':g.photo_set.all()[0].get_thumb(),
                'ratio':'%0.2lf' %(float(g.photo_set.all()[0].thumbdim()[0])/float(g.photo_set.all()[0].thumbdim()[1])),
                'title':g.title, 'fullurl':g.photo_set.all()[0].url() }
                for g in gallerys if g.photo_set.count() > 0 ]
        if stop < len(ret_val['list']):
            ret_val['list'] = ret_val['list'][start:stop]
        else:
            ret_val['list'] = ret_val['list'][start:]
        return ret_val
        
    def gallery_details(self, offset, limit):
        ret_val, offset, limit, count = {}, int(offset), int(limit), Gallery.objects.count()
        gallerys = Gallery.objects.all()
        start, stop = offset, offset+limit
        if count < stop:
            stop = count

        for g in gallerys[start:stop]:
            try:
                ordering = PhotoPlace.objects.filter(gallery__id__exact=g.id) #.order_by('place')
                ret_val[str(g.id)] = [ { 'url':o.photo.url(), 'title':o.photo.title } for o in ordering ]
            except PhotoPlace.DoesNotExist:
                continue
        return ret_val

service = Service()
