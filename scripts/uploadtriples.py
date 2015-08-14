__author__ = 'lorenzo'

#
# Dumps vocabularies into remote datastore with POST requests via cURL
#

import os
from os.path import dirname
from rdflib import Graph
import pycurl
from urllib import urlencode
from config import _TEMP_SECRET

url = 'http://rdfendpoints.appspot.com/ds'


def _curling(url, params):
    """
    POST to a remote url
    :param url: target url
    :param params: parameters in the request
    :return: None
    """
    c = pycurl.Curl()
    c.setopt(c.URL, url)

    post_data = params
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

    c.perform()
    c.close()
    return None


def _dumping(fullpath):
    """
    Create a RDFLib graph from a N-Triples file
    :param fullpath: path of the file
    :return: the Graph instance
    """
    with open(fullpath, 'r') as f:
        g = Graph()
        g.parse(data=f.read(), format="nt")
    return g

basepath = os.path.join(dirname(dirname(os.path.abspath(__file__))), 'RDFvocab', 'ntriples')
print basepath
vocabularies = ((_dumping(os.path.join(path, filename)), filename) for path, dirs, files in os.walk(basepath) for filename in files if filename.endswith(".ntriples"))


for v, f in vocabularies:
    for stmt in v:
        g = Graph()
        g.add(stmt)
        triple = g.serialize(format='nt')
        #print triple
        _curling(url=url, params={'pwd': _TEMP_SECRET, 'triple': triple})


