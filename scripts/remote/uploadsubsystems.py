"""
Main Script for generating and converting JSON to JSON-LD about components for subsystems
(to be dumped and uploaded as triples)
"""

__author__ = 'lorenzo'

import sys
import json

from scripts.datagenerator.constraints import tech_constrains
from scripts.factory import SubSystem


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


def _upload_subsystems(url, n):
    """
    upload to server the subsystems instances
    NOTE: dumped via a REST endpoint /database that has not been created yet
    :param url: the server endpoint
    :param n: number of iteration per family to be generated
    :return:
    """
    for i in range(0, n):
        # generate py instance components and translate in JSON-LD format
        jsons = [SubSystem.generate_py_instance(k, v) for k, v in tech_constrains.items()]
        jsonlds = [SubSystem.generate_jsonld(c) for c in jsons]

        # dump in triples
        from RDFvocab.script.make_n3 import _curling
        translator = 'http://rdf-translator.appspot.com/convert/json-ld/nt/content'
        for j in jsonlds:
            triples = _curling(translator, {'content': json.dumps(j)})
            print triples

            # upload to datastore (under construction)
            # from remote import dump_to_endpoint_post
            # dump_to_endpoint_post(url=url, data=triples)


if __name__ == "__main__":
    _upload_subsystems(sys.argv[1], sys.argv[2])
