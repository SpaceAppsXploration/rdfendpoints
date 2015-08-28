__author__ = 'lorenzo'

from urllib import urlencode

subj, pred, obj = '?s', '?p', '?o'

base = 'SELECT * WHERE { %s %s %s }'

#
# Property "orbitsPlanet"
#
# Solar System
# Which planet is Enceladus orbiting?
test1 = base % ('<http://ontology.projectchronos.eu/solarsystem/Enceladus>', '<http://ontology.projectchronos.eu/astronomy/orbitsPlanet>', '?o')  # result 'Saturn'

# Which satellites orbit Saturn?
test2 = base % ('?s', '<http://ontology.projectchronos.eu/astronomy/orbitsPlanet>', '<http://ontology.projectchronos.eu/solarsystem/Saturn>')  # result *satellites of Saturn*

# What is the Sun?
test3 = base % ('<http://ontology.projectchronos.eu/solarsystem/Sun>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '?o')
# wants more info? Check if "rdfs:subClassOf" and/or "owl:sameAs" are present

# What is Mercury?
test4 = base % ('<http://ontology.projectchronos.eu/solarsystem/Mercury>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '?o')

# What is a Star?
test5 = base % ('<http://ontology.projectchronos.eu/astronomy/Star>', ' <http://www.w3.org/2000/01/rdf-schema#subClassOf>', '?o')
# if type is "owl:Class" check for "rdfs:subClassOf" and/or "owl:sameAs"



print(test2)
