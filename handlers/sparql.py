import webapp2
from config.config import _CLIENT_TOKEN
from flankers.graphtools import query, store_triples

__author__ = ['niels', 'Lorenzo']


class Querying(webapp2.RequestHandler):
    """
    /sparql GET: responds to SPARQL queries using the ?query= parameter
    /sparql POST: endpoint to store triples in the datastore
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
        if self.request.get('token') == _CLIENT_TOKEN:
            # use graphtools.store_triples()
            app_graph, cache_graph = store_triples(self.request.get('triple'))
            return self.response.write("GRAPH STORED OK: {} triples".format(len(cache_graph)))
        return self.response.set_status(405)
