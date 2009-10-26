from rt_www.photogallery.models import Photo, PhotoPlace

class Service:
    def delete_photo(self, pid):
        try:
		photo = Photo.objects.get(pk=pid)
	except Photo.DoesNotExist, e:
		raise e
	""" Here we need to get all the galleries this is ordered in and delete their entries.  Order will be preserved with holes """
	ordering = PhotoPlace.objects.filter(photo__id__exact=photo.id)
	for o in ordering:
		o.delete()
	photo.delete()
        return pid

service = Service()
