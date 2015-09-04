import unittest
from scripts.remote.remote import get_curling, post_curling
from config.config import _ENV

__author__ = 'Lorenzo'


class HTTPendpointsTest(unittest.TestCase):

    def test_sparql(self, env='offline'):
        base_url = _ENV[env]['_SERVICE'] + "/ds"
        queries = ['SELECT * WHERE { ?satellites <http://ontology.projectchronos.eu/astronomy/orbitsPlanet> <http://ontology.projectchronos.eu/solarsystem/Saturn>. }'
                   'SELECT * WHERE { ?satellites <http://ontology.projectchronos.eu/astronomy/orbitsPlanet> ?planets. }',
                   'SELECT * WHERE { ?planets <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontology.projectchronos.eu/astronomy/TerrestrialPlanet> . }']
        responses = [get_curling(base_url, {'query': q}) for q in queries]

        for i, r in enumerate(responses):
            print i, r





