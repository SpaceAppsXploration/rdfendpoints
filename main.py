"""
Main entrypoint for the chronostriples app.
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
from config.config import _PATH, _DEBUG

#
# utilities that are used inside handlers are in flankers/
#
from flankers.graphtools import query

#
# handlers loaded from handlers/
#
from handlers.sparql import Querying
from handlers.componentjsonapi import Endpoints
from handlers.articlesjsonapi import Articles
from handlers.servicehandlers import Testing, Crawling

#
# hydra handlers loaded from hydra/
#
from hydra.handlers import HydraVocabulary, PublishContexts, PublishEndpoints


class Hello(webapp2.RequestHandler):
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


application = webapp2.WSGIApplication([
    webapp2.Route('/test', Testing),
    webapp2.Route('/visualize/articles/', Articles),
    webapp2.Route('/database/cots/<keywd:\w*>', Endpoints),
    webapp2.Route('/database/crawling/store', Crawling),
    webapp2.Route('/sparql', Querying),
    webapp2.Route('/hydra/vocab', HydraVocabulary),
    webapp2.Route('/hydra/contexts/<name:\w+.>', PublishContexts),
    webapp2.Route('/hydra/spacecraft/<name:\w*>', PublishEndpoints),
    webapp2.Route('/', Hello),
], debug=_DEBUG)

