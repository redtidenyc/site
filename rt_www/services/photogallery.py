from photologue.models import Photo, Gallery
# from rt_www.photogallery.models import Photo, Gallery, PhotoPlace

class Service:
    def get_thumb(self, pid):
        return Photo.objects.get(pk=pid).get_thumb()
    def gallery_view(self, offset, limit):
        ret_val, offset, limit = {'count':Gallery.objects.count(), 'list':[]}, int(offset), int(limit)
        gallerys = Gallery.objects.all().order_by('-date_added')
        start, stop = offset, offset+limit
        if ret_val['count'] < stop:
            stop = ret_val['count']
        ret_val['list'] = [ { 'gid':g.id, 'thumburl':g.public()[0].get_thumbnail_url(),
                # 'ratio':'%0.2lf' %(float(g.photos().all()[0].thumbdim()[0])/float(g.photos().all()[0].thumbdim()[1])),
                'title':g.title, 'fullurl':g.public()[0].image.url 
                }
                for g in gallerys if g.photo_count(True) > 0 ]
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
                # ordering = PhotoPlace.objects.filter(gallery__id__exact=g.id).order_by('place')
                # ordering = Photo.objects.filter(public_galleries__id__exact=g.id)
                ret_val[str(g.id)] = [ { 'url': photo.image.url, 'title': photo.title } for photo in g.public() ]
            except Photo.DoesNotExist:
                continue
        return ret_val

service = Service()
