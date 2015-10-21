import unittest
import json
from scripts.remote.remote import get_curling, post_curling
from config.config import _ENV, _CLIENT_TOKEN, _ENV


__author__ = 'Lorenzo'


def test_integrity(res):
    try:
        res = json.loads(res)
        if 'error' not in res.keys():
            return res
        else:
            raise Exception
    except Exception:
        print "the endpoint response was in the wrong format or status 400 or 500"
        print res
        assert False


class HTTPEndpoints(unittest.TestCase):
    def __init__(self, env=None):
        super(HTTPEndpoints, self).__init__()
        if env is not None:
            self.test_env = env
        else:
            self.test_env = 'offline'


class Endpoints_SPARQL(HTTPEndpoints):
    def test_sparql(self):
        """
    Test content of the /database/cots/ endpoint and if contained urls are reachable
    :param env: 'offline' for localhost, 'online' for remote
    """
        print "Running test_sparql"
        env = self.test_env
        base_url = _ENV[env]['_SERVICE'] + "/sparql"
        #
        queries = ["SELECT * WHERE { ?satellites <http://ontology.projectchronos.eu/astronomy/orbitsPlanet> ?planets. }",
                   "SELECT * WHERE { ?planets <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontology.projectchronos.eu/astronomy/TerrestrialPlanet> . }",
                   "SELECT * WHERE { ?satellites <http://ontology.projectchronos.eu/astronomy/orbitsPlanet> <http://ontology.projectchronos.eu/solarsystem/Saturn>. }",
                   "SELECT * WHERE { <" + _ENV[env]['_SERVICE'] + "/data/webresource/5891733057437696> ?p ?o. }"]
        responses = [get_curling(base_url, {'query': q}) for q in queries]

        for i, r in enumerate(responses):
            print i, r
            test_integrity(r)

    def runTest(self):
        run = Endpoints_SPARQL(env='online')
        run.test_sparql()


class Endpoints_Articles(HTTPEndpoints):
    def test_articles_api_base_view(self):
        """
    Test the Articles JSON API: /articles/<version>/
    """
        _VERSION = "v04"
        print "Running test_articles"
        import urllib
        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/articles/" + _VERSION + "/"

        first = get_curling(base_url)
        first = test_integrity(first)

        bookmark = first['next']
        print bookmark
        for i in range(0, 600):  # higher the second element of the interval to test more pages
            print i
            if bookmark:
                count_ = 0
                response = urllib.urlopen(bookmark).read()
                response = test_integrity(response)
                for a in response['articles']:
                    # print a['uuid']
                    count_ += 1

                bookmark = response['next']
                print count_, i, bookmark
            else:
                print 'Articles finished'
                return None

    def test_articles_api_type_view(self):
        """
    Test the Articles JSON API: /articles/<version>/?type_of=
    """
        _VERSION = "v04"
        print "Running test_articles TYPE_OF"
        import urllib
        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/articles/" + _VERSION + "/by?type=feed"

        first = get_curling(base_url)
        first = test_integrity(first)

        bookmark = first['next']
        print bookmark
        for i in range(0, 600):  # higher the second element of the interval to test more pages
            print i
            if bookmark:
                count_ = 0
                response = urllib.urlopen(bookmark).read()
                response = test_integrity(response)
                for a in response['articles']:
                    # print a['uuid']
                    count_ += 1

                bookmark = response['next']
                print count_, i, bookmark
            else:
                print 'Articles by_type finished'
                return None

    def runTest(self):
        run = Endpoints_Articles(env='online')
        run.test_articles_api_base_view()
        run.test_articles_api_type_view()


class Endpoints_Indexer(HTTPEndpoints):
    def test_indexer_base(self):
        _VERSION = "v04"
        print "Running test_indexer_base"

        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/articles/" + _VERSION + "/indexer"

        response = get_curling(base_url)
        test_integrity(response)

        print "Counted keywords: " + str(json.loads(response)['n_indexed'])

    def runTest(self):
        run = Endpoints_Indexer(env='online')
        run.test_indexer_base()


class Endpoints_N3(HTTPEndpoints):
    def test_n3_endpoints(self):
        """
    Test the N3
    """
        print "Running test_n3_endpoints"
        env = self.test_env

        base_url_resource = _ENV[env]['_SERVICE'] + "/datastore/webresource"
        base_url_concept = _ENV[env]['_SERVICE'] + "/datastore/concept"

        test_concepts = []


        response = post_curling(base_url_resource, {"token": _CLIENT_TOKEN})

        print response

        pass

    def runTest(self):
        run = Endpoints_N3(env='online')
        run.test_n3_endpoints()






