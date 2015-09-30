import unittest
import json
from rdflib import Graph

from scripts.remote.remote import get_curling, post_curling
from config.config import _CLIENT_TOKEN, _ENV, _SERVICE, _WEBRES_GRAPH_ID, _CONCEPTS_GRAPH_ID


__author__ = 'Lorenzo'


class BulkOperations(unittest.TestCase):
    def __init__(self, env=None):
        super(BulkOperations, self).__init__()
        if env is not None:
            self.test_env = env
        else:
            self.test_env = 'offline'

    def download_ids_generator(self, results=(), bookmark='start', environment='offline'):
        """
        Recursive - Fetch and collect all the resources' ids in the datastore
        :param results: list of the collected ids
        :param bookmark: bookmark to fetch different datastore's pages
        :return: results list

        # USAGE
            >>> iterated = download_ids_generator(environment='offline')
            >>> for uuid in iterated:
            >>>     print uuid
            >>>     next(iterated)

        """
        import itertools

        to_append = get_curling(_ENV[self.test_env]['_SERVICE'] + '/datastore/index',
                                {'token': _CLIENT_TOKEN,
                                 'bookmark': bookmark if bookmark != 'start' else ''})
        to_append = json.loads(to_append)

        if not to_append['next']:
            return itertools.chain(results, iter(to_append['articles']))

        return self.download_ids_generator(
            results=itertools.chain(results, iter(to_append['articles'])),
            bookmark=to_append['next']
        )

    def create_webresource_triple(self, uuid):
        """
        Create chronos:webresource object for the triple store
        :param uuid: the unique id of the webresource
        :return: a RDF-lib triple (tuple)
        """
        from rdflib import URIRef
        from rdflib.namespace import RDF

        subject = str(_SERVICE + '/data/webresource/' + str(uuid))
        subject = URIRef(subject)
        robject = URIRef('http://ontology.projectchronos.eu/chronos/webresource')

        return subject, RDF.type, robject

    def create_concepts_triples(self, uuid):
        """
        Fetch concepts related to a webresource and create triples
        :param uuid: the unique id of the webresource
        :return:
        """
        from rdflib import URIRef

        concepts = get_curling(
            _ENV[self.test_env]['_SERVICE'] + '/datastore/concepts',
            {
                'retrieve': uuid,
                'token': _CLIENT_TOKEN
            }
        )
        concepts = json.loads(concepts)['concepts']

        triples = []
        if concepts:
            for c in concepts:
                subject = _SERVICE + '/data/concept/' + c
                subject = URIRef(subject)
                predicate = URIRef('http://ontology.projectchronos.eu/chronos/relConcept')
                robject = _SERVICE + '/data/webresource/' + str(uuid)
                robject = URIRef(robject)
                triples.append((subject, predicate, robject))

        return triples

    def dump_webresources_to_graph(self, list_of_ids, url):
        """
        Take a list of unique ids, create a graph of webresources, serialize it to triples and dump them to the
        right graph in the shard.
        :param list_of_ids: a list() of numerical ids from the datastore
        :param url: the url of the sparql endpoint of the shard
        :return: None
        """
        g = Graph()

        for uuid in list_of_ids:
            print uuid
            g.add(self.create_webresource_triple(uuid))

        triples = g.serialize(format='nt')
        post_curling(url,
                     {'token': _CLIENT_TOKEN,
                      'triple': triples,
                      'graph_id': _WEBRES_GRAPH_ID},
                     display=True
                     )

    def dump_concepts_to_graph(self, list_of_ids, url):
        """
        Take a list of unique ids, create a graph of concepts, serialize it to triples and dump them to
        right graph in the shard.
        :param list_of_ids: a list() of numerical ids from the datastore
        :param url: the url of the sparql endpoint of the shard
        :return: None
        """
        g = Graph()

        for uuid in list_of_ids:
            [g.add(c) for c in self.create_concepts_triples(uuid)]

        triples = g.serialize(format='nt')
        post_curling(url,
                     {'token': _CLIENT_TOKEN,
                      'triple': triples,
                      'graph_id': _CONCEPTS_GRAPH_ID},
                     display=True
                     )

    def fetch_and_dump_webresources(self, bookmark='start'):
        """
        Recursive - Fetch all the resources' ids in the datastore and dump it into the triple store.
        Dump also the related keywords/concept in the datastore.
        :param bookmark: bookmark to fetch different datastore's pages
        :return: None
        """
        print "Fetching page: " + bookmark
        to_append = get_curling(_ENV[self.test_env]['_SERVICE'] + '/datastore/index',
                                {'token': _CLIENT_TOKEN,
                                 'bookmark': bookmark if bookmark != 'start' else ''})
        to_append = json.loads(to_append)

        shard_url = _ENV[self.test_env]['_SERVICE'] + '/sparql'

        # dump the single WebResource in the dedicated graph
        self.dump_webresources_to_graph(list_of_ids=to_append['articles'], url=shard_url)

        # dump the concepts related to this webresource in the dedicated graph
        self.dump_concepts_to_graph(list_of_ids=to_append['articles'], url=shard_url)

        if not to_append['next']:
            return None

        return self.fetch_and_dump_webresources(
            bookmark=to_append['next']
        )

    def runTest(self):
        run = BulkOperations(env='offline')
        run.fetch_and_dump_webresources()
