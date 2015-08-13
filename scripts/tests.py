__author__ = 'lorenzo'

import json

from factory import SubSystem, Communication
from constraints import tech_constrains

print " --- attributes in a test object of class Communication"
c = Communication()
for v in vars(c):
    print v

print " --- some attrs printing"
print c.slug
print c.name

print " --- Testing is_constraint()"
print c.is_constraint(c.mass)  # True
print c.is_constraint(c.cost)  # True
print c.is_constraint(c.name)  # False
print c.is_constraint(c.slug)  # False

print " --- full test for generating components and dumping one of them in JSON-LD"
jsons = [SubSystem.generate_instance(k, v) for k, v in tech_constrains.items()]
jsonlds = [SubSystem.generate_jsonld(c) for c in jsons]

print json.dumps(jsonlds, indent=4)

print " --- Translating the component into ntriples"
from RDFvocab.script.make_n3 import _curling
url = 'http://rdf-translator.appspot.com/convert/json-ld/nt/content'
_curling(url, {'content': json.dumps(jsonlds)})
