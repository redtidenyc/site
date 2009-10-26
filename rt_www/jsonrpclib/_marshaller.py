from _errors import ResponseError
import urlparse, simplejson, re

class JSONUnmarshaller:
    def __init__(self):
        self._stack = [] #Arg stack
        self._data = [] #Raw text
        self._methodname = None
        self._encoding = 'uft-8'
        self._decoder = simplejson.JSONDecoder()
        self._type = ''
        self._id = None
        self._obj = None
    def close(self):
        if self._type is None:
            raise ResponseError
        if self._type == 'fault':
            raise Fault(**self._stack[0])
        return tuple(self._stack)
    def end(self):
        self._data = re.sub('[\r\n]+', '', ''.join(self._data))
        if len(self._data) != 0:
            self._obj = self._decoder.decode(self._data)
            try:
                self._stack = self._obj['params']
            except KeyError:
                self._stack = [ Fault('103', 'Malformed request missing params keyword') ]
                self._type = 'fault'
            try:
                self._id = self._obj['id']
            except KeyError:
                pass
    def set_id(self, id):
        self._id = id
    def get_id(self):
        if self._id is not None:
            return self._id
        else:
            return '0'
    def get_args(self):
        return tuple(self._stack)
    def getmethodname(self, url):
        """ There are two possibilities here
            1. We got a GET
            2. We got a POST

            If self._data is nonempty then we received a post.  Anything after the ? is tossed.
            Else we assume a GET a build the self._stack accordingly
        """
        if len(self._data) == 0:
            o = urlparse.urlparse(url).query
            args = [ tuple(arg.split('=')) for arg in o.split('&') if arg != '' ]
            """ 
                We need to handle the case where a GET request has arrays like:
                foo=a&bar=b&foo=c => arg(foo, bar) => arg([a,c], b)
                At least this is my reading of section 6.3.1 of 
                http://json-rpc.org/wd/JSON-RPC-1-1-WD-20060807.html 
            """
            processed_args = []
            while len(args):
                if len(args) > 1:
                    arg, args = args[0], args[1:]
                else:
                    arg, args = args[0], []
                
                if arg[0] in [ a[0] for a in args ]:
                    vals = []
                    del_ind = []
                    for i, a in enumerate(args):
                        if a[0] == arg[0]:
                            vals.append(a[1])
                            del_ind.append(i)
                    for i in del_ind:
                        del args[i]
                    self._stack.append(vals)
                else:
                    self._stack.append(arg[1])
        path = urlparse.urlparse(url)[2]
        self._methodname = '_'.join([ p for p in path.split('/') if p != '' ])
        try:
            self._methodname += '_' + self._obj['method']
        except KeyError:
            pass
        #We got a POST or the GET has been processed
        #The returned function path is like foo_bar => foo.bar
        #If this is a problem, by all means convert it back after you get it out or override this
        return self._methodname

    def data(self, text):
        self._data.append(text)
