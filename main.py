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

from flankers.graphtools import query, store_triples
from flankers.errors import format_message
from config import _TEMP_SECRET, _PATH, _DEBUG
from datastore.models import Component

# generic tools are in tools.py module
# tools using Graph() and NDBstore are in graphtools.py module


class Hello(webapp2.RequestHandler):
    """
    / Homepage
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
    /ds GET: responds to SPARQL queries using the ?query= parameter
    /ds POST: endpoint to store triples in the datastore
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
    /database/cots/ GET: Serves (HATEOAS) JSON objects from the datastore, mostly COTS components
    /database/cots/store POST: store component instance in the datastore
    """
    def get(self, keywd):
        from flankers.tools import valid_uuid, families

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'
        if not keywd:
            # keywd is None serves Entrypoint
            from config import _VOCS, _REST_SERVICE
            results = [{"name": f[f.rfind('_') + 1:],
                        "collection_ld+json_description": _VOCS['subsystems'] + f + '/' + '?format=jsonld',
                        "collection_n-triples_description": _VOCS['subsystems'] + f,
                        "go_to_collection": _REST_SERVICE + f}
                       for f in families]
            return self.response.write(json.dumps(results, indent=2))
        elif keywd == 'ntriples' and self.request.get('uuid'):
            # url is "url/cots/ntriples?key=<uuid>"
            uuid = self.request.get('uuid')
            if valid_uuid(uuid):
                # return ntriples of the object
                return self.response.write(format_message("N-Triples not yet implemented"))
        elif valid_uuid(keywd):
            # if the url parameter is an hex, this should be a uuid
            # print a single component (in JSON with a link to N-Triples)
            if self.request.get('format') and self.request.get('format') == 'jsonld':
                # if user asks for JSON-LD
                self.response.headers['Content-Type'] = 'application/ld+json'
                try:
                    body = Component.parse_to_jsonld(keywd)
                except ValueError as e:
                    return self.response.write(format_message(e))
                return self.response.write(body)
            else:
                # serve JSON
                try:
                    body = Component.parse_to_json(keywd)
                except ValueError as e:
                    return self.response.write(format_message(e))
                return self.response.write(body)

        elif keywd in families:
            # if the url parameter is a family name
            # print the list of all the components in that family
            results = Component.get_by_collection(keywd)
            return self.response.write(results)
        else:
            # wrong url parameters
            return self.response.write(format_message("Not a valid key/id in URL"))

    def post(self, keywd):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        if keywd == 'store' and self.request.get('pwd') == _TEMP_SECRET:
            jsonld = self.request.get('data')
            from datastore.models import Component
            key = Component.dump_from_jsonld(jsonld)
            return self.response.write("COMPONENT STORED OK: {}".format(key))
        else:
            self.response.status = 405
            return self.response.write('Not Authorized')


class Crawling(webapp2.RequestHandler):
    """
    Service handler for operations on crawled resources
    """
    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        if self.request.get('pwd') == _TEMP_SECRET and self.request.get('resource'):
            from datastore.models import WebResource
            try:
                oid = WebResource.dump_from_json(self.request.get('resource'))
            except (Exception, ValueError) as e:
                self.response.status = 400
                return self.response.write('The request could not be understood, wrong resource format or syntax: ' + str(e))
            self.response.status = 200
            return self.response.write('Resource Stored: ' + str(oid))
        else:
            self.response.status = 405
            return self.response.write('Not Authorized')


class FourOhFour(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(404)

application = webapp2.WSGIApplication([
    webapp2.Route('/test', Testing),
    webapp2.Route('/database/cots/<keywd:\w*>', Endpoints),
    webapp2.Route('/database/crawling/store', Crawling),
    webapp2.Route('/ds', Querying),
    webapp2.Route('/', Hello),
], debug=_DEBUG)

