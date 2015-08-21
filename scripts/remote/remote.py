"""
Tools for remote interaction with the server/datastore
"""

__author__ = 'lorenzo'

import sys
sys.path.insert(0, '../..')
from config import _TEMP_SECRET


def dump_to_ds_post(url, data):
    """
    open a connection and dump via POST to /ds
    :param url: the server url
    :param data: the triples
    :return: urllib response
    """
    import urllib
    params = urllib.urlencode({'pwd': _TEMP_SECRET, 'triple': data})
    f = urllib.urlopen(url, params)
    print f.read()


def dump_to_endpoint_post(url, data):
    """
    open a connection and dump via POST to /database endpoint
    UNDER-CONSTRUCTION
    :param url: the server url
    :param data: the triples
    :return: urllib response
    """
    import urllib
    params = urllib.urlencode({'pwd': _TEMP_SECRET, 'data': data})
    f = urllib.urlopen(url, params)
    print f.read()
