import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext as Context
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

from rt_www.photogallery.models import Gallery, Photo, PhotoPlace
from rt_www.swimmers.models import Swimmer

def index(request):
    c= Context(request, {'cl':ChangeList(request, Gallery)})
    return render_to_response('photogallery/admin/index.html', {}, context_instance=c)
index = staff_member_required(never_cache(index))

def change_gallery(request, add = None, gid = None):
    new_data = errors = {}
    gallery = None
    context_args = {'aphotos':Photo.objects.filter(gallery__isnull=True)}
    if gid:
        context_args['cphotos'] = Photo.objects.filter(gallery__id__exact=int(gid))
        try:
            context_args['gallery'] = Gallery.objects.get(pk=gid)
        except Gallery.DoesNotExist:
            errors.append(_('The Gallery was not found'))

    if request.POST:
        new_data = request.POST.copy()
        images_to_add = [ int(im_id) for im_id in new_data['keep_ims'].split(',') if im_id != '' ]
        images_to_disassociate = [ int(im_id) for im_id in new_data['disassoc_ims'].split(',') if im_id != '' ]
        user = None
        if new_data.has_key('swimmer'):
            try:
                user = User.objects.get(pk=new_data['swimmer'])
            except User.DoesNotExist:
                pass

        if not errors:
            if gid:
                try:
                    gallery = Gallery.objects.get(pk=gid)
                    gallery.title = new_data['title']
                    gallery.creator = user
                except Gallery.DoesNotExist:
                    gallery = Gallery(title=new_data['title'], creator=user)
                gallery.save()
            else:
                gallery = Gallery(title=new_data['title'], creator=user)
                gallery.save()

            """ First thing we do is clear out any old ordering sitting about """
            places = PhotoPlace.objects.filter(gallery__id__exact=gallery.id)
            for p in places:
                p.delete()

            for d in images_to_disassociate:
                try:
                    photo = Photo.objects.get(pk=d)
                    gallery.photo_set.remove(photo)
                except Photo.DoesNotExist:
                    continue
                except Gallery.DoesNotExist: #This should never happen
                    continue

            for i, image_id in enumerate(images_to_add):
                try:
                    photo = Photo.objects.get(pk=image_id)
                except Photo.DoesNotExist:
                    continue
                gallery.photo_set.add(photo)
                p = PhotoPlace(gallery=gallery, photo=photo, place=i)
                p.save()
            gallery.save()

            LogEntry.objects.log_action(request.user.id,
                ContentType.objects.get_for_model(Gallery).id, gallery.id, str(gallery), CHANGE)
            msg = _('The %(name)s "%(obj)s was successfully modified') \
                %{ 'name':Gallery._meta.verbose_name, 'obj':gallery }
            if request.POST.has_key("_continue"):
                request.user.message_set.create(message=msg + ' ' + _("You may edit it again below."))
                return HttpResponseRedirect('/admin/photogallery/gallery/%d/' % int(gallery.id))
            elif request.POST.has_key("_addanother"):
                request.user.message_set.create(message=msg + ' ' + (_("You may add another %s below.") \
                    % Photo._meta.verbose_name))
                """ FIXME: I didn't have an internet connection but we need to set this path
                    to the base path of the image
                """
                return HttpResponseRedirect('/admin/photogallery/gallery/add/')
            else:
                request.user.message_set.create(message=msg)
                return HttpResponseRedirect('/admin/photogallery/gallery/')
    if gallery is not None:
        context_args['gallery'] = gallery

    if add == 'add':
        context_args['add'] = True
    else:
        context_args['change'] = True

    c = Context(request, context_args)
    return render_to_response('photogallery/admin/gallery_form.html', {}, context_instance=c)

change_gallery = staff_member_required(never_cache(change_gallery))

def delete_gallery(request, gid) :
    new_data = errors = {}
    try:
        gallery = Gallery.objects.get(pk=gid)
    except Gallery.DoesNotExist:
        msg = _('The Gallery was not found')
        request.user.message_set.create(message=msg)
        return HttpResponseRedirect('/admin/photogallery/gallery/')
    msg = _('The Gallery %s was deleted' % gallery)
    request.user.message_set.create(message=msg)
    for photo in gallery.photo_set.all():
        photo.gallery = None
        photo.save()
    gallery.delete()
    return HttpResponseRedirect('/admin/photogallery/gallery/')

delete_gallery = staff_member_required(never_cache(delete_gallery))
