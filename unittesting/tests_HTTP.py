import unittest
import json
from scripts.remote.remote import get_curling, post_curling
from config.config import _ENV
from flankers.tools import families

__author__ = 'Lorenzo'


class HTTPendpointsTest(unittest.TestCase):

    def test_sparql(self, env='online'):
        """
    Test content of the /database/cots/ endpoint and if contained urls are reachable
    :param env: 'offline' for localhost, 'online' for remote
    """
        base_url = _ENV[env]['_SERVICE'] + "/ds"
        #
        queries = ["SELECT * WHERE { ?satellites <http://ontology.projectchronos.eu/astronomy/orbitsPlanet> ?planets. }",
                   "SELECT * WHERE { ?planets <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontology.projectchronos.eu/astronomy/TerrestrialPlanet> . }",
                   "SELECT * WHERE { ?satellites <http://ontology.projectchronos.eu/astronomy/orbitsPlanet> <http://ontology.projectchronos.eu/solarsystem/Saturn>. }"]
        responses = [get_curling(base_url, {'query': q}) for q in queries]

        for i, r in enumerate(responses):
            print i, r
            try:
                json.loads(r)
                assert True
            except Exception:
                print "the endpoint response was in the wrong format or status 400 or 500"
                assert False

    def test_json(self, env='offline'):
        """
    Test content of the /database/cots/ endpoint and if contained urls are reachable
    :param env: 'offline' for localhost, 'online' for remote
    """
        import urllib

        base_url = _ENV[env]['_SERVICE'] + "/database/cots/"
        response = get_curling(base_url)
        print response
        response = json.loads(response)
        props = ["go_to_collection", "collection_ld+json_description", "collection_n-triples_description", "name"]
        names = [f.split('_')[1] for f in families]
        for r in response:
            assert all(True if rp in props else False for rp in [k for k in r.keys()])
            print "Testing urls in the response. Wait..."
            assert all(urllib.urlopen(v).getcode() == 200
                       if k != 'name'
                       else v in names
                       for k, v in r.items())







