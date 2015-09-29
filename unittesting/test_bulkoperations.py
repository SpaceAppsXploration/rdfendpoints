import unittest
import json
from scripts.remote.remote import get_curling
from config.config import _CLIENT_TOKEN, _ENV, _SERVICE

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

    '''
    iterated = download_ids_generator(environment='offline')
    for uuid in iterated:
        print uuid
        next(iterated)
    '''


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

    # dump_to_triple_store()


    def dump_to_graph(self, list_of_ids, url):
        """
        Take a list of unique ids, create a graph of triples and dump them to the shard
        :param list_of_ids: a list() of numerical ids from the datastore
        :param url: the url of the sparql endpoint of the shard
        :return: None
        """
        from scripts.remote.remote import post_curling
        from rdflib import Graph

        g = Graph()

        for uuid in list_of_ids:
            g.add(self.create_webresource_triple(uuid))

        triples = g.serialize(format='nt')
        post_curling(url,
                     {'token': _CLIENT_TOKEN, 'triple': triples,
                      'graph_id': 'webresources-graph'},
                     display=True
                     )

    def fetch_and_dump_ids(self, bookmark='start'):
        """
        Recursive - Fetch all the resources' ids in the datastore and dump it into the triple store
        :param bookmark: bookmark to fetch different datastore's pages
        :return: None
        """
        print "Fetching page: " + bookmark
        to_append = get_curling(_ENV[self.test_env]['_SERVICE'] + '/datastore/index',
                                {'token': _CLIENT_TOKEN,
                                 'bookmark': bookmark if bookmark != 'start' else ''})
        to_append = json.loads(to_append)

        shard_url = _ENV[self.test_env]['_SERVICE'] + '/sparql'
        self.dump_to_graph(list_of_ids=to_append['articles'], url=shard_url)

        if not to_append['next']:
            return None

        return self.fetch_and_dump_ids(
            bookmark=to_append['next']
        )

    def runTest(self):
        run = BulkOperations(env='offline')

        run.fetch_and_dump_ids()