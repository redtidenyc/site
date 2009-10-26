"""
    This follows the example set xmlrpclib.py
"""

import simplejson

FAILURE = 500

class Error(Exception):
    """ Base class of client errors """
    def __str__(self):
        return repr(self)

class ResponseError(Error):
    """ Indicates a broken response package """
    pass

"""
    indicates a JSON-RPC fault response package.  This exception is raised 
    by the unmarshalling layer.  This exception can also be used as a class,
    to generate a fault JSON-RPC message.
    @param faultCode The JSON-RPC fault code
    @param faultString the JSON-RPC fault string.

"""

class Fault(Error):
    """ Indicates an JSON-RPC fault package """
    def __init__(self, faultCode, faultString, **extra):
        Error.__init__(self)
        self.faultCode = faultCode
        self.faultString = faultString
    def __repr__(self):
        return simplejson.dumps({ 'name':'JSONRPCError', 'code':self.faultCode, 'message':self.faultString })
