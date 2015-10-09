import unittest
import urllib
import json

__author__ = 'Lorenzo'

from config.youtube_secret import _KEY
from scripts.remote.remote import get_curling

url = 'https://www.googleapis.com/youtube/v3/search'
params= {
    'part': 'id, snippet',
    'q': ['space+exploration', 'space race', 'space', 'astrophysics', 'astronomy'],
    'type': 'video',
    'videoCategoryId': 35, # documentary
    'key': _KEY
}

def fetch_data_q():
    """
    Search for videos using query parameter
    :return:
    """
    data = urllib.urlencode({
            'part': params['part'],
            'q': params['q'][0],
            'maxResult': 3,
            'key': _KEY
        })
    request = url + '?' +data
    response = urllib.urlopen(
        request
    )
    return response.read()


def fetch_data_title():
    """
    Search for videos using as parameters some random titles
    :return:
    """
    from datastore.videos import videos  # a list of 120 titles

    for v in videos:
        q = v['title']
        data = urllib.urlencode({
            'part': params['part'],
            'q': q,
            'maxResult': 15,
            'key': _KEY
        })
        request = url + '?' +data
        response = urllib.urlopen(
            request
        )
        return response.read()


def store_video(obj):
    print obj

def store_response(resp):
    for video in resp.items:
        store_video(video)


response = fetch_data()

#store_response(response)

# note: pageToken = response.nextPageToken
print json.loads(response)