import os.path, md5, Image, os, subprocess

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Video(models.Model):
    video = models.FilePathField(path='%s/videos' % settings.MEDIA_ROOT, editable=False, match='[a-z0-9]+\.flv', recursive=False)
    thumbfile = models.FilePathField(path='%s/videos/thumbs' % settings.MEDIA_ROOT, editable=False, match='[a-z0-9]+\.png', recursive=False)
    title = models.CharField(_('Title'), max_length=256, blank=True, null=True)
    comment = models.CharField(_('Comment'), max_length=256, blank=True)
    photographer = models.ForeignKey(User, blank=True, null=True)
    date_uploaded = models.DateField(_('Date Uploaded'), auto_now_add=True)
    class Meta:
        verbose_name_plural = _('Videos')

    def __unicode__(self):
        if not self.title:
            return ''
        return self.title
    def thumb_link(self):
        return '<img src="%s" border="0" alt=""/>' % self.get_thumb()

    thumb_link.allow_tags = True
    thumb_link.short_description = 'Video'

    def get_video(self):
        return '/media/videos/%s' % os.path.split(self.video)[1]

    def get_thumb(self):
        return '/media/videos/thumbs/%s' % os.path.split(self.thumbfile)[1]

    def save(self):
        """
            Couple steps in here.  We check to see if the file is an avi file.  If so we convert it to a flv.
            Second we pull the first frame for a screen capture.
            if thumbfile is set we assume this has already been done
        """

        if self.thumbfile == '':
            """ make filename """
            f = open(self.video, 'rb')
            data = f.read(1000)
            f.close()
            m = md5.new()
            m.update(data)
            nvname = '%s/videos/%s.flv' %( settings.MEDIA_ROOT, m.hexdigest() )
            self.thumbfile = '%s/videos/thumbs/%s.png' %( settings.MEDIA_ROOT, m.hexdigest() )
            ret = subprocess.Popen('/usr/bin/ffmpeg -i %s -acodec mp3 -ar 22050 -ab 32 -f flv -s 320x240 %s; /usr/bin/ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 320x240 %s; /usr/bin/flvtool2 -U %s; rm %s' %( self.video, nvname, nvname, self.thumbfile, nvname, self.video), shell=True)
            self.video = nvname

        super(Video, self).save()

    def delete(self):
        try:
            os.unlink(self.video)
            os.unlink(self.thumbfile)
        except Exception, e:
            print e
            pass
        super(Video, self).delete()

class Gallery(models.Model):
    title = models.CharField(_("Title"), max_length=80)
    date = models.DateField(_("Publication Date"), auto_now_add=True)
    creator = models.ForeignKey(User, verbose_name=_("Gallery Created by"), blank=True, null=True )

    class Meta:
        get_latest_by = 'date'
        verbose_name_plural = _('Galleries')

    def __unicode__(self):
        return self.title

    def get_admin_url(self):
        return '/admin/photogallery/'

class Photo(models.Model):
    image = models.CharField(_("Photograph"), editable=False, max_length=512, blank=True, null=True)
    title = models.CharField(_("Title"), max_length=80, blank=True)
    desc = models.TextField(_("Description"), blank=True)
    gallery = models.ForeignKey(Gallery, null=True, blank=True)
    photographer = models.ForeignKey(User, null=True, verbose_name=_("Photographer"), blank=True)
    date = models.DateField(_("Date Photographed"), blank=True, null=True)

    class Meta:
        ordering = ( '-date', )

    class Admin:
        list_display = ( 'thumb', 'title', 'photographer', 'gallery',)
        list_filter = ( 'gallery', )
        list_display_links = ( 'thumb', )
        js = ('js/MochiKit/MochiKit.js', 'js/autocomplete.js', 'js/admin/PhotoManager.js',)

    def __str__(self):
        return self.title

    def thumb(self):
        return '<img src="%s" border="0" alt=""/>' % self.get_thumb()

    thumb.allow_tags = True
    thumb.short_description = 'Image'

    def __get_base(self, path, head):
        tail, head_new = os.path.split(path)
        if head_new == 'media':
            return head
        elif head == '':
            return self.__get_base(tail, head_new)
        else:
            return self.__get_base(tail, head_new + '/' + head)

    def get_thumb(self):
        base_path = os.path.split(self.__get_base(self.image, ''))[0]
        file = 'thumb_' + os.path.split(self.__get_base(self.image, ''))[1]
        return '/media/' + base_path + '/' + file

    def url(self):
        base_path = os.path.split(self.__get_base(self.image, ''))[0]
        file = os.path.split(self.__get_base(self.image, ''))[1]
        return '/media/' + base_path + '/' + file

    def delete(self):
        thumb = os.path.split(self.image)[0] + '/thumb_' + os.path.split(self.image)[1]
        try:
            os.unlink(thumb)
        except:
            pass

        try:
            os.unlink(self.image)
        except:
            pass
        super(Photo, self).delete()
    def save(self):
        data = ''
        if self.image != '':
            f = open(self.image, 'rb')
            data = f.read()
            f.close()
        m = md5.new()
        m.update(data)
        self.image = '%sphotos/%s.jpg' %( settings.MEDIA_ROOT, m.hexdigest() )
        f = open(self.image, 'wb')
        f.write(data)
        f.close()
        im = Image.open(self.image)
        format = im.format
            # Make a copy of the image, scaled, if needed.
        maxwidth = 640
        maxheight = 480
        width, height = im.size
        newim = im
        if (width > maxwidth) and width > height:
            scale = float(maxwidth)/width
            width = int(width * scale)
            height = int(height * scale)
            try:
                newim = im.resize( (width, height), Image.ANTIALIAS )
            except IOError:
                pass
        elif (height > maxheight) and height >= width:
            scale = float(maxheight)/height
            width = int(width * scale)
            height = int(height * scale)
            try:
                newim = im.resize( (width, height), Image.ANTIALIAS )
            except IOError:
                pass
        newim.save(self.image, format)

        thumbsize = 165, 125
        maxwidth = 165
        maxheight = 125
        outpath = '%s/photos/thumb_%s.jpg' %( settings.MEDIA_ROOT, m.hexdigest())
        try:
            im = Image.open(self.image)
            format = im.format
            width, height = im.size
            if (width > maxwidth) and (width > height):
                scale = float(maxwidth)/width
                width = int(width * scale)
                height = int(height * scale)
                newim = im.resize( (width, height), Image.ANTIALIAS )
            elif (height > maxheight):
                scale = float(maxheight)/height
                width = int(width * scale)
                height = int(height * scale)
                newim = im.resize( (width, height), Image.ANTIALIAS )
            else:
                newim = im
                newim.save(outpath, format)
        except IOError:
            print "cannot create thumbnail for", self.image

            super(Photo, self).save()

    def thumbdim(self):
        thumb = os.path.split(self.image)[0] + '/thumb_' + os.path.split(self.image)[1]
        im = Image.open(thumb)
        return im.size

class PhotoPlace(models.Model):
    gallery = models.ForeignKey(Gallery)
    photo = models.ForeignKey(Photo)
    place = models.IntegerField(_('Place'))
    class Meta:
        unique_together = (('gallery', 'photo', 'place'),)
