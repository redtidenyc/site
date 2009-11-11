from django.conf import settings
from django.http import HttpResponse
from rt_www import jsonrpclib
import os, re, sys
class JSONRPCMiddleware:
    """
        This piece of middleware implements the Non-Standard JSON RPC standard for the django framework
        However it does *not* implement GET calls due to security issues raised by
        http://www.fortifysoftware.com/servlet/downloads/public/JavaScript_Hijacking.pdf

        For the JSON-RPC semi standard see: http://json-rpc.org/wiki/specification

        This middleware obeys a couple variables from settings
        ROOT            : this is the path on the filesystem to where the services and adminservices are installed
                          if this is set then SERVICES and ADMINSERVICES are ignored
        SERVICES        : the path for the services directory
        ADMINSERVICES   : the path for the adminservices directory.  Adminservices are the same as services
                          except they are hooked into the django authentication mechanism.  The expectation
                          here is that staff is true and these are json calls for use in the admin

        Laying out services --

        The layout in both directories looks something like:
        ROOT/service/module.py
        and inside module.py:
        class Service:
            def method(self, arg):
                #stuff
        service = Service()

        Upon instantiation this middleware goes through each directory and attaches each method for the service object
        to itself like: self._service__module__method(self, arg)
        so the request /services/module/ with the method to execute in the POST is transformed into this call

        Finally we need a couple access requirements.  If the method has a .login_required = True attribute then
        the user must be logged to use the remote method
        .staff_required => .login_required and also means the user must have is_staff == True
    """
    def __init__(self):
        try:
            root = getattr(settings, 'ROOT')
            self.services = '%s/services' % root
            self.adminservices = '%s/adminservices' % root
            sys.path += [root]
        except AttributeError:
            try:
                self.services, self.adminservices = getattr(settings, 'SERVICES'), getattr(settings, 'ADMINSERVICES')
                sys.path += [self.services + '/../', self.adminservice + '/../']
            except AttributeError:
                raise Exception('Either ROOT or SERVICES and ADMINSERVICES must be declared in your settings.py')
        self.__modules = []
        self.__load_modules(self.services, 'services')
        self.__load_modules(self.adminservices, 'adminservices')
        print self.__modules

    def __load_modules(self, path, type):
        """ load all the submodules from each """
        print path
        print type
        for f in os.listdir(path):
            print f
        mod_names = [ re.sub('.py', '', f ) for f in os.listdir(path) if re.search('^[^_].*?\.py$', f) ]
        print mod_names
        for name in mod_names:
            try:
                m = __import__('%s.%s' %(type, name), globals(), locals(), ['service'])
                globals()['service'] = getattr(m, 'service')
                for m in dir(service):
                    method = getattr(service, m)
                    if callable(method):
                        self.__dict__['_%s_%s_%s' %(type, name, m)] = method
                self.__modules.append('%s_%s' %( type, name))
            except AttributeError:
                continue
            except ImportError:
                continue


    def __isrpcpath(self, requestpath):
        root = '_'.join([ p for p in requestpath.split('/') if p != '' ])
        return root in self.__modules
    def __getmethod(self, funcpath):
        try:
            return getattr(self, '_%s' % funcpath)
        except AttributeError:
            return None

    def process_request(self, request):
        """
        This takes a post request of the form
        /services/<module>/ and executes the attached method.
        anything in /adminservices/ requires staff status
        """
        if request.method == 'POST' and self.__isrpcpath(request.path):
            parser, unmarshaller = jsonrpclib.getparser()
            parser.feed(request.raw_post_data)
            parser.close()

            args, id, funcpath = unmarshaller.close(), unmarshaller.get_id(), unmarshaller.getmethodname(request.path)
            func = self.__getmethod(funcpath)

            ret_val = { 'version':'1.1', 'id':id }

            try:
                if [ p for p in request.path.split('/') if p != ''][0] == 'adminservices':
                    if not ( request.user.is_authenticated() and request.user.is_staff ):
                        ret_val['error'] = {'name':'JSONRPCError', 'code':jsonrpclib.FAILURE, 'message':'Permission Denied'}
                try:
                    lrequired = getattr(func, 'login_required')
                    if lrequired and not request.user.is_authenticated():
                        ret_val['error'] = {'name':'JSONRPCError', 'code':jsonrpclib.FAILURE, 'message':'Permission Denied'}
                    args = tuple([ a for a in args ] + [ request ])
                except AttributeError:
                    pass

                try:
                    isstaff = getattr(func, 'staff_required')
                    if isstaff and not ( request.user.is_authenticated() and request.user.is_staff ):
                        ret_val['error'] = {'name':'JSONRPCError', 'code':jsonrpclib.FAILURE, 'message':'Permission Denied'}
                    args = tuple([ a for a in args ] + [ request ])
                except AttributeError:
                    pass

                ret_val['result'] = func(*args)
            except Exception, e:
                ret_val['error'] = {'name':'JSONRPCError', 'code':jsonrpclib.FAILURE, 'message':'%s' % e}

            return HttpResponse(jsonrpclib.dumps(ret_val), mimetype='application/javascript')
