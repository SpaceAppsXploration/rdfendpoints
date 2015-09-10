import unittest
import json
from scripts.remote.remote import get_curling, post_curling
from config.config import _ENV
from flankers.tools import families

__author__ = 'Lorenzo'


def test_integrity(res):
    try:
        res = json.loads(res)
        return res
    except Exception:
        print "the endpoint response was in the wrong format or status 400 or 500"
        assert False


class HTTPendpointsTest(unittest.TestCase):
    def __init__(self, env=None):
        super(HTTPendpointsTest, self).__init__()
        if env is not None:
            self.test_env = env
        else:
            self.test_env = 'offline'

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
                   "SELECT * WHERE { ?satellites <http://ontology.projectchronos.eu/astronomy/orbitsPlanet> <http://ontology.projectchronos.eu/solarsystem/Saturn>. }"]
        responses = [get_curling(base_url, {'query': q}) for q in queries]

        for i, r in enumerate(responses):
            print i, r
            test_integrity(r)

    def test_json(self):
        """
    Test content of the /database/cots/ endpoint and if contained urls are reachable
    :param env: 'offline' for localhost, 'online' for remote
    """
        print "Running test_json"
        import urllib
        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/database/cots/"
        response = get_curling(base_url)
        response = json.loads(response)
        props = ["go_to_collection", "collection_ld+json_description", "collection_n-triples_description", "name"]
        names = [f.split('_')[1] for f in families]
        for r in response:
            assert all(True if rp in props else False for rp in [k for k in r.keys()])
            print "Testing urls in the response. Wait..."
            assert all(urllib.urlopen(v).getcode() == 200 or urllib.urlopen(v).getcode() == 301
                       if k != 'name'
                       else v in names
                       for k, v in r.items())

    def test_jsonld(self):
        """
    Test the hypermedia endpoints: /hydra/spacecraft/
    """
        print "Running test_jsonld"
        import urllib
        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/hydra/spacecraft/"
        response = urllib.urlopen(base_url).read()
        test_integrity(response)

    def test_articles(self):
        """
    Test the NL API: /visualize/articles/?api=true
    """
        print "Running test_articles"
        import urllib
        env = self.test_env

        base_url = _ENV[env]['_SERVICE'] + "/visualize/articles/"

        first = get_curling(base_url, {'api': 'true'})
        first = test_integrity(first)

        bookmark = first['next']
        print bookmark
        for i in range(0, 5):
            print i
            response = urllib.urlopen(bookmark).read()
            response = test_integrity(response)
            bookmark = response['next']
            print i, bookmark

    def runTest(self):
        run = HTTPendpointsTest(env='online')
        run.test_sparql()
        run.test_json()
        run.test_jsonld()
        run.test_articles()






