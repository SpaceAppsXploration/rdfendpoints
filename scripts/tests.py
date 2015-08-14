__author__ = 'lorenzo'

import json
import unittest

from factory import SubSystem, Communication
from constraints import tech_constrains


class BasicObjectCreation(unittest.TestCase):
    kind = 'communication'
    c = Communication(
        SubSystem.generate_instance(kind, tech_constrains['communication'])
    )  # create a random object, generating data from technical constraints

    def test_create_object(self):
        print " --- attributes in a test object of class Communication"

        for v in vars(self.c):
            print v + '> ', getattr(self.c, v)
        print " --- some attrs printing"
        print self.c.name
        print getattr(self.c, "subsystems:hasMass")
        print getattr(self.c, "subsystems:hasMonetaryValue")
        print self.c.name
        print self.c.id

    def test_dumping_pipe_single(self):
        pass

    def test_dumping_pipe_full(self):
        print " --- full test for generating components and dumping them in JSON-LD"
        jsons = [SubSystem.generate_instance(k, v) for k, v in tech_constrains.items()]
        jsonlds = [SubSystem.generate_jsonld(c) for c in jsons]

        print json.dumps(jsonlds, indent=4)

        print " --- Translating the component into ntriples via RDFtranslator"
        from RDFvocab.script.make_n3 import _curling
        url = 'http://rdf-translator.appspot.com/convert/json-ld/nt/content'
        _curling(url, {'content': json.dumps(jsonlds)})

    def runTest(self):
        pass

    def test_run_basic(self):
        t = BasicObjectCreation()
        t.test_create_object()
        del t

    def test_run_pipe(self):
        t = BasicObjectCreation()
        t.test_dumping_pipe_full()
        del t


class FactoryTest(unittest.TestCase):
    def test_generate_object(self):
        from generator import generate_object

        specs = tech_constrains['propulsion']
        kind = 'propulsion'

        print json.dumps(generate_object(kind, specs), indent=4)