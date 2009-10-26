"""
    The jsonrpclib module.  The interface is based heavily on the xmlrpclib.  works alot the same
"""

from _errors import Fault, FAILURE
from _marshaller import JSONUnmarshaller
from _parser import JSONParser
import simplejson

def getparser():
    target = JSONUnmarshaller()
    parser = JSONParser(target)
    return parser, target

def dumps(struct):
    return simplejson.dumps(struct)
