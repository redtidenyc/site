from zope.interface import implements, Interface
from twisted.application import internet, service
from twisted.internet import defer
from twisted.python import failure
from twisted.cred import portal, checkers, credentials, error as credError
from twisted.protocols import ftp
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rt_www.photogallery.models import Photo, Video
from django.conf import settings
from django.contrib.sessions.models import Session

import tempfile, datetime, os, os.path, md5, Image, re
import cStringIO as StringIO


"""
    This ftp server works in two ways.
    1. Plain old login - we get a username and password and dump the user inside the MEDIA_ROOT
    2. Session cookie - we get a url like ftp.redtidenyc.org/<sid>/
    This is where we leverage the coupling between django and the ftp server.  If the user has a valid session in the admin
    we authenticate using the preestablished credentials

    The avatars are simple here.  They are simply a user and a filsystem root which is always hard coded to the MEDIA_ROOT
    and a list of directories they are allowed to see.  All access is rw for now
"""

class _PhotoWriter(ftp._FileWriter):
    def __init__(self):
        self.buffer = StringIO.StringIO()
        self._receive = False
    def receive(self):
        assert not self._receive, "Can only call IWriteFile.receive *once* per instance"
        self._receive = True
        # FileConsumer will close the file object
        return defer.succeed(PhotoConsumer(self.buffer))

class _VideoWriter(ftp._FileWriter):
    def __init__(self, ext):
        self.tfd, self.fname = tempfile.mkstemp(dir='%s/videos' % settings.MEDIA_ROOT, suffix=ext)
        self._receive = False
    def receive(self):
        assert not self._receive
        self._receive = True
        return defer.succeed(VideoConsumer(self.tfd, self.fname))

class VideoConsumer(ftp.FileConsumer):
    def __init__(self, fd, fname):
        self.tfd, self.fname = fd, fname
    def unregisterProducer(self):
        self.producer = None
        os.close(self.tfd)
        v = Video(video=self.fname)
        v.save()
        """ We don't unlink the tempfile in here because there is alot of latency here """
    def write(self, bytes):
        os.write(self.tfd, bytes)


class PhotoConsumer(ftp.FileConsumer):
    def __init__(self, buffer):
        self.buffer = buffer
    def unregisterProducer(self):
        self.producer = None
        #Now we save the file after renaming it to the md5sum
        tfd, fname = tempfile.mkstemp(dir='%s/tmp' % settings.ROOT)
        os.write(tfd, self.buffer.getvalue())
        self.buffer.close()
        os.close(tfd)
    p = Photo(image=fname)
        p.save()
        try:
            os.unlink(fname)
        except:
            pass
    def write(self, bytes):
        self.buffer.write(bytes)

class RTFTPShell(ftp.FTPShell):
    allowed_dirs = ['pdfs', 'uploads', 'photos', 'videos', 'flash', 'backups' ]
    def list(self, path, keys=()):
        is_allowed = False
        if len(path) == 0:
            is_allowed = True
        else:
            for seg in path:
                if seg in self.allowed_dirs:
                    is_allowed = True
                    break
        results = []
        if is_allowed:
            path = self._path(path)
            if path.isdir():
                entries = path.listdir()
            else:
                entries = [None]

            for fName in entries:
                if not fName or re.search('^\.', str(fName)):
                    continue
                ent = []
                full_path = os.path.join(path.path, fName)
                if not os.path.isdir(full_path) or fName in self.allowed_dirs:
                    results.append((fName, ent))
                if keys:
                    if fName is not None:
                        p = os.path.join(path.path, fName)
                    else:
                        p = path.path
                    try:
                        statResult = os.stat(p)
                    except (IOError, OSError), e:
                        return ftp.errnoToFailure(e.errno, path)
                    except:
                        return defer.fail()

                for k in keys:
                    ent.append(getattr(self, '_list_' + k)(statResult))

        return defer.succeed(results)
    def removeFile(self, path):
        in_photo_dir, in_video_dir = False, False
        for seg in path:
            if seg == 'photos':
                in_photo_dir = True
            elif seg == 'videos':
                in_video_dir = True

        p = self._path(path)
        if in_photo_dir:
            try:
                photo = Photo.objects.get(image__exact=p.path)
                photo.delete()
            except Photo.DoesNotExist:
                try:
                    p.remove()
                except:
                    return defer.fail()
        elif in_video_dir:
            try:
                video = Video.objects.get(video__exact=p.path)
                video.delete()
            except Video.DoesNotExist:
                try:
                    p.remove()
                except:
                    return defer.fail()
        else:
            try:
                p.remove()
            except:
                return defer.fail()
        return defer.succeed(None)

    def openForWriting(self, path):
        in_photo_dir, in_video_dir = False, False
        for seg in path:
            if seg == 'photos':
                in_photo_dir = True
            elif seg == 'videos':
                in_video_dir = True

        filename = path[-1]
        p = self._path(path)
        ext = os.path.splitext(filename)[1].lower()
        if in_photo_dir and ext in [ '.jpeg', '.jpg' ]:
            return defer.succeed(_PhotoWriter())
        if in_video_dir and ext in [ '.flv', '.avi' ]:
            return defer.succeed(_VideoWriter(ext))
        else:
            return ftp.FTPShell.openForWriting(self, path)


class ISession(credentials.ICredentials):
    """The django session checker is inside here

    """

class RTSession:
    implements(ISession)
    def __init__(self, sid):
        self.session_id = sid

class RedtideFTPRealm(ftp.FTPRealm):
    def requestAvatar(self, avatarId, mind, *interfaces):
        for iface in interfaces:
            if iface is ftp.IFTPShell:
                if avatarId is checkers.ANONYMOUS:
                    avatar = ftp.FTPAnonymousShell(self.anonymousRoot)
                else:
                    avatar = RTFTPShell(self.anonymousRoot)
                return ftp.IFTPShell, avatar, getattr(avatar, 'logout', lambda: None)

        raise NotImplementedError("Only IFTPShell interface is supported by this realm")

class RedtideUPAuthenticator:
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword, credentials.IAnonymous, )

    def requestAvatarId(self, credentials):
        if not hasattr(credentials, 'username'):
            return checkers.ANONYMOUS
        return defer.maybeDeferred(self.login, credentials.username, credentials.password)

    def login(self, username, password):
        user = authenticate(username=username, password=password)
        if ( user is not None ) and ( user.is_active and user.is_staff ):
            return username
        else:
            raise credError.UnauthorizedLogin()

class RedtideSessionAuthenticator:
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = ( ISession, )

    def requestAvatarId(self, credentials):
        return defer.maybeDeferred(self.login, credentials.session_id)
    def login(self, sid):
        try:
            s = Session.objects.get(pk=sid, expire_date__gte=datetime.datetime.now())
            u = User.objects.get(pk=s.get_decoded()['_auth_user_id'])
            return u.username
        except User.DoesNotExist:
            raise credError.UnauthorizedLogin()
        except Session.DoesNotExist:
            raise credError.UnauthorizedLogin()

class RTFTP(ftp.FTP):


    def processCommand(self, cmd, *params):
        cmd = cmd.upper()
        if self.state == self.UNAUTH:
            if cmd == 'USER':
                return self.ftp_USER(*params)
            elif cmd == 'PASS':
                return ftp.BAD_CMD_SEQ, "USER required before PASS"
            else:
                return ftp.NOT_LOGGED_IN

        elif self.state == self.INAUTH:
            if cmd == 'PASS':
                return self.ftp_PASS(*params)
            else:
                return ftp.BAD_CMD_SEQ, "PASS required after USER"

        elif self.state == self.AUTHED:
            method = getattr(self, "ftp_" + cmd, None)
            if method is not None:
                if self._user != self.factory.userAnonymous:
                    return method(*params)
                elif cmd == 'CWD':
                    return self.path_auth(*params)
                else:
                    return ftp.CMD_OK
            return defer.fail(ftp.CmdNotImplementedError(cmd))

        elif self.state == self.RENAMING:
            if cmd == 'RNTO':
                return self.ftp_RNTO(*params)
            else:
                return ftp.BAD_CMD_SEQ, "RNTO required after RNFR"

    def ftp_PASS(self, password):
        """
        Second part of login.  Get the password the peer wants to
        authenticate with.
        """
        if self.factory.allowAnonymous and self._user == self.factory.userAnonymous:
            # anonymous login
            creds = credentials.Anonymous()
            reply = ftp.GUEST_LOGGED_IN_PROCEED
        else:
            # user login
            creds = credentials.UsernamePassword(self._user, password)
            reply = ftp.USR_LOGGED_IN_PROCEED

        def _cbLogin((interface, avatar, logout)):
            assert interface is ftp.IFTPShell, "The realm is busted, jerk."
            self.shell = avatar
            self.logout = logout
            self.workingDirectory = []
            self.state = self.AUTHED
            return reply

        def _ebLogin(failure):
            failure.trap(credError.UnauthorizedLogin, credError.UnhandledCredentials)
            self.state = self.UNAUTH
            raise ftp.AuthorizationError

        d = self.portal.login(creds, None, ftp.IFTPShell)
        d.addCallbacks(_cbLogin, _ebLogin)
        return d

    def path_auth(self, path):
        reply = ftp.USR_LOGGED_IN_PROCEED
        creds = RTSession(path)
        self._user = path
        def _cbLogin((interface, avatar, logout)):
            assert interface is ftp.IFTPShell, "The realm is busted, jerk."
            self.shell = avatar
            self.logout = logout
            self.workingDirectory = []
            self.state = self.AUTHED
            return reply
        def _ebLogin(failure):
            failure.trap(credError.UnauthorizedLogin, credError.UnhandledCredentials)
            self.state = self.UNAUTH
            raise ftp.AuthorizationError

        d = self.portal.login(creds, None, ftp.IFTPShell)
        d.addCallbacks(_cbLogin, _ebLogin)
        return d

class RedtideFTPFactory(ftp.FTPFactory):
    protocol = RTFTP
    allowAnonymous = True
    welcomeMessage = 'Redtide\'s Own FTP Server'

def main():
    app = service.Application('Redtide FTP Server')

    p = portal.Portal(RedtideFTPRealm(settings.MEDIA_ROOT))
    p.registerChecker(RedtideUPAuthenticator())
    p.registerChecker(RedtideSessionAuthenticator())

    internet.TCPServer(21, RedtideFTPFactory(p)).setServiceParent(app)
    return app

application = main()
