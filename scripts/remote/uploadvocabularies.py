"""
Dumps vocabularies into remote datastore with POST requests.
Usage examples:
    python uploadvocabularies.py http://localhost:10080/sparql
    python uploadvocabularies.py http://localhost:8080/sparql
    python uploadvocabularies.py http://chronostriples.appspot.com/sparql
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

