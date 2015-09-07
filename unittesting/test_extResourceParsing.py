import unittest
import json
from scripts.remote.remote import get_curling, post_curling
from flankers.graphtools import query

__author__ = 'Lorenzo'


class externalResourceTest(unittest.TestCase):


    def getDBpediaN3(self):
        """
        test if DBpedia ntriples retrieval is working
        :return:
        """
        results = get_curling('http://hypermedia.projectchronos.eu/sparql', {
            'query': 'SELECT * WHERE { ?planets <http://www.w3.org/1999/02/22-rdf-syntax-ns#type><http://ontology.projectchronos.eu/astronomy/Planet> . }'
        })
        results = json.loads(results)
        print results['results']['bindings']
        urls = [r['planets']['value'] for r in results['results']['bindings']]
        print urls[0]

        def get_link(url):
            rdf = get_curling(url, {'format': 'jsonld'})
            rdf = json.loads(rdf)
            sameas = rdf['owl:sameAs']
            return sameas

        from flankers.extCaching import dbpedia_url

        n3s = dict()
        for u in urls:
            l = get_link(u)
            j = dbpedia_url(l)
            n3s[j] = get_curling(j)

        return n3s

    def test_dbpedia_url(self):
        """
        test function flankers.extCaching.dbpedia_url
        :return:
        """
        from flankers.extCaching import dbpedia_url

        test = [
            [{u'@id': u'http://umbel.org/umbel/rc/PlanetMercury'}, {u'@id': u'http://live.dbpedia.org/data/Mercury_(planet).ntriples'}, {u'@id': u'http://sw.opencyc.org/2012/05/10/concept/en/PlanetMercury'}],
            [{u'@id': u'http://live.dbpedia.org/data/Ceres_(dwarf_planet).ntriples'}]
        ]

        assertion = ['http://live.dbpedia.org/data/Mercury_(planet).ntriples',
                     'http://live.dbpedia.org/data/Ceres_(dwarf_planet).ntriples']

        for i, t in enumerate(test):
            assert dbpedia_url(t) == assertion[i]



    def runTest(self):
        run = externalResourceTest()
        print run.getDBpediaN3()