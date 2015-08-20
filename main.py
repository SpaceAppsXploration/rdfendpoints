# -*- coding: utf-8 -*-
"""
FORKED FROM https://github.com/mr-niels-christensen/rdflib-appengine/blob/master/src/example/httpserver.py
"""
import os
import sys
sys.path.insert(0, 'lib')

import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from rdflib import Graph
from ndbstore import NDBStore
import urllib
from json2html import *
import json
import logging

from config import _GRAPH_ID, _TEMP_SECRET, _VOCS, _PATH, _SERVICE


class MainPage(webapp2.RequestHandler):
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
            cache_graph = Graph()
            cache_graph.parse(data = self.request.get('triple'),
                              format="nt")
            app_graph = Graph(store=NDBStore(identifier=_GRAPH_ID))
            app_graph += cache_graph
            return self.response.write("GRAPH STORED OK: {} triples".format(len(cache_graph)))
        return self.response.set_status(405)


class testing(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('test')


class endpoints(webapp2.RequestHandler):
    def get(self, vocabulary, predicate, value):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        base = 'select * where { %s %s ?y }' \
               % ('<' + _VOCS['solarsystem'] + '/' + value + '>', '<' + _VOCS[vocabulary] + '/' + predicate + '>')
        self.response.write(base)
        #return self.response.write(query(base))


class Hello(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        path = os.path.join(_PATH, 'index.html')
        return self.response.out.write(template.render(path, {}))

    def post(self):
        if self.request.get('query'):
            #url = _SERVICE + '?' + urllib.urlencode({'query': self.request.get('query')})
            #try:
            #    result = urlfetch.fetch(url)
            #except Exception:
            #    self.response.headers['Content-Type'] = 'text/plain'
            #    return self.response.write('Query have run out of time, retry or try another one')

            jcontent = json.loads(query(self.request.get('query')))
            params = {
                'result': json2html.convert(json=jcontent['results']),
                'status': 200,
                'query': urllib.unquote(self.request.get('query')).decode('utf8')
            }
            path = os.path.join(_PATH, 'index.html')
            return self.response.out.write(template.render(path, params))
        return self.response.set_status(405)


class FourOhFour(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(404)

application = webapp2.WSGIApplication([
    webapp2.Route('/test', testing),
    webapp2.Route('/rest/<vocabulary>/<predicate>/<value>', endpoints),
    webapp2.Route('/ds', MainPage),
    webapp2.Route('/', Hello),
], debug=True)


def update(q):
    graph().update(q)


def query(q):
    response = graph().query(q)
    if response.type == 'CONSTRUCT': #These cannot be JSON-serialized so we extract the data with a SELECT
        g = Graph()
        g += response
        response = g.query("SELECT ?s ?p ?o WHERE {?s ?p ?o}")
    return response.serialize(format='json')
    

def graph():
    return Graph(store=NDBStore(identifier=_GRAPH_ID))