"""
Multi-purpose handler to manage the triple store's entities and references
"""

from google.appengine.ext import ndb
from datastore.models import WebResource, Indexer

from handlers.basehandler import ServiceHandler
from config.config import _CLIENT_TOKEN, _SERVICE, _WEBRES_GRAPH_ID, _VOC_GRAPH_ID
from flankers.graphtools import store_triples

__author__ = 'Lorenzo'


class DataToTriplestore(ServiceHandler):
    """
    Perform different actions of the triple store:
    1. Dump: store from WebResource to triple store
    2. Monitor: return statistics on the triple store
    """

    @classmethod
    def n_triplify(cls, dictionary):
        """
        Translate a dictionary with defined structure into a
        string containing ntriple.

        :param dictionary:
           {
              "subject": <url of the subject>,
              "predicate": <url of a predicate>,
              "object": <url of the object>
           }
        :return: a string containing well-formatted ntriple

        """

        subject = str('<' + dictionary['subject'] + '> ')  # add subject
        results = subject
        results += '<' + dictionary['predicate'] + '> '  # predicate
        results += '<' + dictionary['object'] + '> .'  # add object

        print results
        return results

    @classmethod
    def build_triples(cls, obj):
        """
        Build dictionaries containing triples to describe a WebResource object
        and its indexed keywords.

        :param obj: a query result from the datastore
        :return: a dict and a list containing dict with a "subject", "predicate",
        "object" properties.
        """
        # build the dictionary to describe the WebResource as a triple
        definition = {
            "subject": _SERVICE + '/data/webresource/' + str(obj.key.id()),
            "predicate": 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
            "object": 'http://ontology.projectchronos.eu/chronos/concept'
        }

        # collect the related concepts of the WebResource and create a list of dictionaries
        # to describe them as triples
        indexed = obj.get_indexers()["keywords"]
        related = []
        for i in indexed:
            rel = {
                "subject": _SERVICE + '/data/webresource/' + str(obj.key.id()),
                "predicate": 'http://ontology.projectchronos.eu/chronos/relConcept',
                "object": _SERVICE + '/data/concept/' + i["slug"]
            }
            related.append(rel)

        return definition, related

    def post(self, perform):
        """
        Handle dumping and monitoring for Triple Store.
        """
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'text/html'

        if self.request.get('token') == _CLIENT_TOKEN:
            # authorized
            if perform == 'dump':
                # dump Webresource
                # 1. get a batch to be dumped
                _BATCH = int(self.request.get('batch'))
                query = WebResource.query(WebResource.in_graph == False).fetch(_BATCH)

                for q in query:
                    triples = str()
                    # 2. create triples representing the resource and its related concepts
                    df, rl = self.build_triples(q)
                    print df, rl
                    triples += self.n_triplify(df)
                    triples += " ".join([self.n_triplify(r) for r in rl])
                    print triples
                    # 3. store triples
                    _, cache_graph = store_triples(triples, _VOC_GRAPH_ID, format="n3")
                    print "GRAPH STORED OK: {} triples".format(len(cache_graph))
                    # 4. set in_graph flag to True
                    q.in_graph = True
                    q.put()

                return self.response.write(
                    "A batch of " + str(_BATCH) +
                    " resources has been successfully stored in the triple store"
                )
            elif perform == 'monitor':
                # gather statistics
                pass
