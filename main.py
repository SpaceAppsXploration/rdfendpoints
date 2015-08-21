# -*- coding: utf-8 -*-
"""
Main entrypoint for the rdfendpoints app

FORKED FROM https://github.com/mr-niels-christensen/rdflib-appengine/blob/master/src/example/httpserver.py
"""

__author__ = ['niels', 'lorenzo']

import os
import sys
sys.path.insert(0, 'lib')

import webapp2
from google.appengine.ext.webapp import template

import urllib
from json2html import *

from graphtools import query, store_triples
from config import _TEMP_SECRET, _PATH

# generic tools are in tools.py module
# tools using Graph() and NDBstore are in graphtools.py module


class Hello(webapp2.RequestHandler):
    """
    /: Homepage
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


class Querying(webapp2.RequestHandler):
    """
    /ds: responds to SPARQL queries using the ?query= parameter
    """
    def get(self):
        if self.request.get('query'):
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
            print(self.request.get('query'))
            return self.response.write(query(self.request.get('query')))
        return self.response.write("Query not defined")

    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        if self.request.get('pwd') == _TEMP_SECRET:
            # use graphtools.store_triples()
            app_graph, cache_graph = store_triples(self.request.get('triple'))
            return self.response.write("GRAPH STORED OK: {} triples".format(len(cache_graph)))
        return self.response.set_status(405)


class Testing(webapp2.RequestHandler):
    """
    /test: test handler
    """
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('test')


class Endpoints(webapp2.RequestHandler):
    """
    Serves (HATEOAS) JSON objects from the datastore, mostly COTS components
    """
    def get(self, keywd):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        from tools import valid_uuid, families

        if keywd == 'ntriples' and self.request.get('uuid'):
            # url is "url/cots/ntriples?uuid=<uuid>"
            uuid = self.request.get('uuid')
            # return ntriples of the object
            pass
        elif valid_uuid(keywd):
            # if the url parameter is an hex, this should be a uuid
            # print a single component (in JSON with a link to N-Triples)
            #
            # { <id>: { name: ...,
            #           mass: ...,
            #           ... : ...,
            #           n-triples: "url/cots/ntriples?uuid=<uuid>" } }
            pass
        elif keywd in families:
            # if the url parameter is a family name
            # print the list of all the components in that family
            pass

        return self.response.write(keywd)


class FourOhFour(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(404)

application = webapp2.WSGIApplication([
    webapp2.Route('/test', Testing),
    webapp2.Route('/database/cots/<keywd>', Endpoints),
    webapp2.Route('/ds', Querying),
    webapp2.Route('/', Hello),
], debug=True)

