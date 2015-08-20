__author__ = 'lorenzo'

#
# Dumps vocabularies into remote datastore with POST requests
#

import sys
import os
from os.path import dirname
import urllib

def _upload_all(url):
    basepath = os.path.join(dirname(dirname(os.path.abspath(__file__))), 'RDFvocab', 'ntriples')
    for path, _dirs, files in os.walk(basepath):
        for filename in files:
            if filename.endswith(".ntriples"):
                fullpath = os.path.join(path, filename)
                print 'Uploading {}...'.format(fullpath)
                with open(fullpath, 'r') as f:
                    data = f.read()
                params = urllib.urlencode({'pwd': '***', 'triple': data})
                f = urllib.urlopen(url, params)
                print f.read()

if __name__ == "__main__":
    #Usage examples:
    #python uploadtriples.py http://localhost:10080/ds
    #python uploadtriples.py http://localhost:8080/ds
    #python uploadtriples.py http://rdfendpoints.appspot.com/ds
    _upload_all(sys.argv[1])

