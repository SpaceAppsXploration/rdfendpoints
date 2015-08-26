"""
Dumps vocabularies into remote datastore with POST requests.
Usage examples:
    python uploadtriples.py http://localhost:10080/ds
    python uploadtriples.py http://localhost:8080/ds
    python uploadtriples.py http://rdfendpoints.appspot.com/ds
"""

__author__ = ['lorenzo', 'niels']

import sys
import urllib

from remote import post_curling
from config.config import _TEMP_SECRET, _VOCS


def _upload_all(url):
    for k, v in _VOCS.items():
        triples = urllib.urlopen(v)
        post_curling(url, {'pwd': _TEMP_SECRET, 'triple': triples.read()}, display=True)

if __name__ == "__main__":
    _upload_all(sys.argv[1])

