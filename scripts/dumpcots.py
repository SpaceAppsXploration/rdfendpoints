"""
Main Script for generating and converting JSON to JSON-LD about components for subsystems
(to be dumped and uploaded as triples)
"""

__author__ = 'lorenzo'


import json
from constraints import tech_constrains

from factory import SubSystem


def generate_metaclasses():
    """
    NOTED FUNCTION - not implemented
    :return:
    """
    classes = {}
    for k, v in tech_constrains.items():
        # doc for type > https://docs.python.org/2/library/functions.html#type
        # usage http://stackoverflow.com/a/15247202/2536357
        classname = "%s" % SubSystem.stringify(k)
        print classname
        classes[classname] = (type(classname, (SubSystem,), v))
    return classes


n = 1  # number of instances per family of components to be generated

# generate components in JSON format
jsons = [SubSystem.generate_instance(k, v) for i in range(0, n) for k, v in tech_constrains.items()]
print json.dumps(jsons, indent=4)

# convert JSON in JSON-LD
jsonlds  = [SubSystem.generate_jsonld(c) for c in jsons]
print json.dumps(jsonlds, indent=4)

# dump in triples
from RDFvocab.script.make_n3 import _curling
url = 'http://rdf-translator.appspot.com/convert/json-ld/nt/content'
_curling(url, {'content': json.dumps(jsonlds)})


# upload to datastore