__author__ = 'lorenzo'

import json
import unittest

from scripts.factory import  SubSystem
from scripts.datagenerator.constraints import tech_constrains
from config import _TEMP_SECRET


class BasicObjectCreation(unittest.TestCase):
    kind = 'communication'
    c = SubSystem.generate_py_instance(kind, tech_constrains['communication'])
    # create a random object, generating data from technical constraints

    @classmethod
    def test_created_object(cls, obj):
        """
        Dumps some attributes of an object to test the content
        :param obj: a class instance
        :return: None
        """
        print " --- attributes in a test object of class Communication"

        for v in vars(obj):
            print v + ' > ', getattr(obj, v)
        print " --- some attrs printing"
        print getattr(obj, "subsystems:hasMass")
        print getattr(obj, "subsystems:hasMonetaryValue")
        print obj.name
        print obj.id

    @classmethod
    def test_dumping_pipe_full(cls):
        """
        Tests creating python instances > dumping JSON-LD > translate into N-TRIPLES
        :return:
        """
        print " --- full test for generating components and dumping them in JSON-LD"
        jsons = [SubSystem.generate_py_instance(k, v) for k, v in tech_constrains.items()]
        jsonlds = [SubSystem.generate_jsonld(c) for c in jsons]

        print json.dumps(jsonlds, indent=4)

        print " --- Translating the component into ntriples via RDFtranslator"
        from RDFvocab.script.make_n3 import _curling
        url = 'http://rdf-translator.appspot.com/convert/json-ld/nt/content'
        _curling(url, {'content': json.dumps(jsonlds)})

    def test_run_basic(self):
        t = BasicObjectCreation()
        t.test_created_object(self.c)
        del t

    def test_run_pipe(self):
        t = BasicObjectCreation()
        t.test_dumping_pipe_full()
        del t

    def runTest(self):
        pass

    def test_post_to_component_endpoint(self):
        """
        WARNING: it stores in the local datastore the json-ld in testdata.component
        :return:
        """
        #from models import Component
        from scripts.testdata.component import component
        from scripts.remote.remote import post_curling

        post_curling(url='http://localhost:8080/database/cots/store',
                     params={'pwd': _TEMP_SECRET, 'data': component},
                     display=True)

        #c = Component.dump_from_jsonld(component)
        #print c


class FactoryTest(unittest.TestCase):

    specs = tech_constrains['detector']
    kind = 'detector'

    @classmethod
    def test_generate_py_object(cls, kind, specs):
        """
        Tests SubSystem.generate_py_instance(kind, specs)
        :param kind:
        :param specs:
        :return:
        """
        obj = SubSystem.generate_py_instance(kind, specs)
        print obj
        BasicObjectCreation.test_created_object(obj)
        return obj

    def test_dumping_pipe_single(self):
        self.test_generate_py_object(self.kind, self.specs)

    def test_dumping_pipe_all_kinds_full(self):
        for k, v in tech_constrains.items():
            self.test_generate_py_object(k, v)

    def test_generate_json_ld_single(self):
        """
        Tests SubSystem.generate_jsonld(obj)
        :return:
        """
        obj = self.test_generate_py_object(self.kind, self.specs)
        print json.dumps(SubSystem.generate_jsonld(obj), indent=4)

    def test_generate_json_ld_all_kinds(self):
        """
        Tests SubSystem.generate_jsonld(obj) for all the subsytems kinds
        :return:
        """
        for k, v in tech_constrains.items():
            obj = self.test_generate_py_object(k, v)
            s = SubSystem.generate_jsonld(obj)
            print json.dumps(s, indent=4)
            print '-*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-'
