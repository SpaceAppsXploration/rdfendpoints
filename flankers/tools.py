"""
Generic tools for handlers operations
"""

__author__ = 'lorenzo'

# from google.appengine.api import urlfetch
import json
from bs4 import BeautifulSoup
import urllib2


families = ['Spacecraft_Detector', 'Spacecraft_Propulsion', 'Spacecraft_PrimaryPower',
            'Spacecraft_BackupPower', 'Spacecraft_Thermal', 'Spacecraft_Structure', 'Spacecraft_CDH',
            'Spacecraft_Communication', 'Spacecraft_AODCS']


def valid_uuid(uuid):
    """
    matches if a string is a valid uuid.hex
    :param uuid:
    :return:
    """
    import re
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(uuid)
    return bool(match)


def retrieve_json(url, method='GET', data=None):
    """
    Utility: URL's body fetching
    :rtype : dict()
    :param url: URL to fetch
    :param method: the method to use for the request
    :param data: if method is POST, pass also some data for request's body
    :return: dictionary from the response's body
    """
    # print url
    if method == 'GET':
        # avoid HTML escaping problems using bs4
        return json.loads(urllib2.urlopen(url).read())
    elif method == 'POST':
        if data is not None:
            import urllib

            data = urllib.urlencode(data)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            return json.loads(response.read().encode('ascii', 'replace'))
        else:
            raise Exception('retrieve_json(): data for POST cannot be None')
    else:
        raise Exception('retrieve_json(): Wrong Method')