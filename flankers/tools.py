#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Generic tools for handlers operations
"""

__author__ = 'lorenzo'

# from google.appengine.api import urlfetch
import json
from bs4 import BeautifulSoup
import urllib2

# #######################
"""
the web url matching regex used by markdown
http://daringfireball.net/2010/07/improved_regex_for_matching_urls
https://gist.github.com/gruber/8891611
"""
URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|info|int|de|us|)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""


def spot_urls(text):
    import re
    return re.findall(URL_REGEX, text)
# ######################


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