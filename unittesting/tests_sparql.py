__author__ = 'lorenzo'


import unittest
from urllib import urlencode


subj, pred, obj = '?s', '?p', '?o'

base = 'SELECT * WHERE { %s %s %s }'


fulltest = []
#
# Property "orbitsPlanet"
#
# Solar System
# Which planet is Enceladus orbiting?
test1 = base % ('<http://ontology.projectchronos.eu/solarsystem/Enceladus>', '<http://ontology.projectchronos.eu/astronomy/orbitsPlanet>', '?o')  # result 'Saturn'
fulltest.append(test1)
# Which satellites orbit Saturn?
test2 = base % ('?s', '<http://ontology.projectchronos.eu/astronomy/orbitsPlanet>', '<http://ontology.projectchronos.eu/solarsystem/Saturn>')  # result *satellites of Saturn*
fulltest.append(test2)
# What is the Sun?
test3 = base % ('<http://ontology.projectchronos.eu/solarsystem/Sun>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '?o')
# wants more info? Check if "rdfs:subClassOf" and/or "owl:sameAs" are present
fulltest.append(test3)
# What is Mercury?
test4 = base % ('<http://ontology.projectchronos.eu/solarsystem/Mercury>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '?o')
fulltest.append(test4)
# What is a Star?
test5 = base % ('<http://ontology.projectchronos.eu/astronomy/Star>', ' <http://www.w3.org/2000/01/rdf-schema#subClassOf>', '?o')
# if type is "owl:Class" check for "rdfs:subClassOf" and/or "owl:sameAs"
fulltest.append(test5)


class SPARQLquery(unittest.TestCase):
    """
    Tests SPARQL locally
    """

    def test_basic_sparql(self):
        from flankers.graphtools import query
        try:
            for t in fulltest:
                print t + "\n" + query(t)
        except Exception:
            assert False


class SPARQLrequest(unittest.TestCase):
    """
    Tests SPARQL remotely
    """
    pass