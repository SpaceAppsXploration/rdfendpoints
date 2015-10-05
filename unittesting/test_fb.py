import unittest
import json
import urllib

from config.fb_secret import fb_appid, fb_secret
from flankers.textsemantics import find_related_concepts
from flankers.fbstore import FBStore
from flankers.tools import spot_urls

__author__ = 'Lorenzo'





class FBTests(unittest.TestCase):
    def test_get(self):
        aliases = ['GuntersSpacePage', 'SETIInstitute']
        url = 'https://graph.facebook.com/GuntersSpacePage/posts?' + FBStore.generate_token()
        response = urllib.urlopen(url)
        response = json.loads(response.read())
        if 'error' not in response.keys():
            print response
            print spot_urls(response['data'][0]['message'])
        else:
            print response['error']['message'], response['error']['type']