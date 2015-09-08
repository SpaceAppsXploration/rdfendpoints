"""
Tools for remote interaction with the server/datastore
"""

__author__ = 'lorenzo'

import sys
sys.path.insert(0, '../..')
from config.config import _TEMP_SECRET


def dump_to_ds_post(url, data):
    """
    open a connection and dump via POST to /ds
    NOTE: better to use PYcURL for this operations, avoid a lot of encoding and conflicts
    :param url: the server url
    :param data: the triples
    :return: urllib response
    """
    import urllib
    params = urllib.urlencode({'pwd': _TEMP_SECRET, 'triple': data})
    f = urllib.urlopen(url, params)
    print f.read()


def post_curling(url, params, file=None, display=False):
    """
    POST to a remote url and print the response in a file or on screen or return the body of the response
    :param url: target url
    :param params: parameters in the request
    :param file: name of the output file
    :param display: true if you want to print output on console/command line
    :return: file > None, body of the response
    """
    import pycurl
    from urllib import urlencode
    from StringIO import StringIO

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    # if request is GET
    #if params: c.setopt(c.URL, url + '?' + urlencode(params))

    # if request is POST
    post_data = params
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

    if file and not display:
        # if a path is specified, it prints on file
        c.setopt(c.WRITEDATA, file)
        c.perform()
        c.close()
        return None
    if display:
        storage = StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        c.close()
        print storage.getvalue()
        return None

    # else it returns a string
    storage = StringIO()
    c.setopt(c.WRITEFUNCTION, storage.write)
    c.perform()
    c.close()
    return storage.getvalue()


def get_curling(url, params={}):
    import pycurl
    import urllib
    from StringIO import StringIO

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.URL, url + '?' + urllib.urlencode(params))
    print urllib.urlencode(params)
    # For older PycURL versions:
    #c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    return body