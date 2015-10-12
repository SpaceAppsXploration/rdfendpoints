"""
Main entrypoint for the chronostriples website.
Publishing at http://hypermedia.projectchronos.eu

FORKED FROM https://github.com/mr-niels-christensen/rdflib-appengine/blob/master/src/example/httpserver.py
"""

__author__ = ['niels', 'lorenzo']

import os
import sys
sys.path.insert(0, 'lib')

import webapp2
import urllib
from google.appengine.ext.webapp import template
from json2html import *

# * generic tools are in tools.py module
# * tools using Graph() and NDBstore are in graphtools.py module
# * handlers are in the handlers/ package

#
# all the static variables are in config/config.py
#
from config.config import _PATH, _DEBUG, _XPREADER_PATH

#
# utilities that are used inside handlers are in flankers/
#
from flankers.graphtools import query

#
# handlers loaded from handlers/
#
from handlers.basehandler import BaseHandler
from handlers.sparql import Querying
from handlers.articlesjsonapi import ArticlesJSONv1
from handlers.servicehandlers import DataStoreOperationsAPI
from handlers.dataN3 import PublishWebResources, PublishConcepts, PublishSpaceDocs


class Hello(BaseHandler):
    """
    / GET: Homepage
    """
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        path = os.path.join(_PATH, 'index.html')
        return self.response.out.write(template.render(path, {}))

    def post(self):
        if self.request.get('query'):
            jcontent = json.loads(query(self.request.get('query')))
            params = {
                'result': json2html.convert(json=jcontent['results']),
                'status': 200,
                'query': urllib.unquote(self.request.get('query')).decode('utf8')
            }
            path = os.path.join(_PATH, 'index.html')
            return self.response.out.write(template.render(path, params))
        return self.response.set_status(405)


class Testing(webapp2.RequestHandler):
    """
    /test: test handler
    """
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        try:
            from bs4 import BeautifulSoup
            from json2html import __version__
        except Exception as e:
            raise e
        self.response.write('test passed')

#
### Handlers Order:
# 1. Test handler
# 2. Keywords Filter-By JSON API
# 3. Articles Filter-By JSON API
# 4. Articles Base JSON API
# 5. Datastore Operations private API
# 6. SPARQL endpoint
# 7. NTriples API (WebResource)
# 8. NTriples API (Taxonomy concepts)
# 9. NTriples API (Taxonomy DBpedia terms)
# 10. Homepage
#

application = webapp2.WSGIApplication([
    webapp2.Route('/test', Testing),
    webapp2.Route('/articles/v04/keywords/by', ArticlesJSONv1),
    webapp2.Route('/articles/v04/by', ArticlesJSONv1),
    webapp2.Route('/articles/v04/', ArticlesJSONv1),
    webapp2.Route('/datastore/<name:[a-z]+>', DataStoreOperationsAPI),
    webapp2.Route('/sparql', Querying),
    webapp2.Route('/data/webresource/<key:[a-zA-Z0-9-_=]+>', PublishWebResources),
    webapp2.Route('/data/concept/<label:[a-z\+]+>', PublishConcepts),
    webapp2.Route('/data/dbpediadocs/<term:[a-z_\(\)-]+>', PublishSpaceDocs),
    webapp2.Route('/', Hello),
], debug=_DEBUG)

