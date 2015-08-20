"""
Dumps vocabularies into remote datastore with POST requests.
Usage examples:
    python uploadtriples.py http://localhost:10080/ds
    python uploadtriples.py http://localhost:8080/ds
    python uploadtriples.py http://rdfendpoints.appspot.com/ds
"""

__author__ = ['lorenzo', 'niels']

import sys
import os
from os.path import dirname

from remote import dump_to_ds_post


def _upload_all(url):
    basepath = os.path.join(dirname(dirname(dirname(os.path.abspath(__file__)))), 'RDFvocab', 'ntriples')
    for path, _dirs, files in os.walk(basepath):
        for filename in files:
            if filename.endswith(".ntriples"):
                fullpath = os.path.join(path, filename)
                print 'Uploading {}...'.format(fullpath)
                with open(fullpath, 'r') as f:
                    data = f.read()
                dump_to_ds_post(url, data)

if __name__ == "__main__":
    _upload_all(sys.argv[1])

