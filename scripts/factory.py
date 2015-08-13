__author__ = 'lorenzo'

import random
import uuid

from constraints import tech_constrains
from generator import generate_object


class SubSystem(object):
    @classmethod
    def stringify(cls, name):
        return name.title().replace(" ", "")

    @classmethod
    def naturify(cls, slug):
        import re
        s = re.sub(r"([A-Z])", r" \1", slug).split()
        return " ".join(s).lower()

    @classmethod
    def generate_instances(cls, kind, specs):
        """
        Take the technical specs of a family of subsystems (communication, propulsion, ...) and create components objects
        :param kind: string representing the kind/family
        :param specs: dictionary of specs taken from constraints
        :return: component as a JSON object
        """
        name = str(random.randrange(0, 200)) + str(random.choice(['T', 'W', 'KV', 'JFG'])) + ' ' + kind
        obj = {'id': uuid.uuid4().hex, 'name': name}
        obj = dict(obj.items() + generate_object(kind, specs).items())
        return obj

    @classmethod
    def generate_jsonld(cls, component):
        """
        Tools for converting a JSON object taken from  generate_instances() to a compacted JSON-LD
        UNDER CONSTRUCTION
        :param component: JSON object as dict
        :return: JSON-LD object as dict
        """
        if isinstance(component, dict):
            raise TypeError

        maps = {
            "subsystems": "http://ontology.projectchronos.eu/subsystems/",
            "iri": "http://ontology.projectchronos.eu/COTS/",
            "mass": "http://sw.opencyc.org/2012/05/10/concept/en/Gram",
            "currency": "http://sw.opencyc.org/2012/05/10/concept/en/Euro",
            "power": "http://dbpedia.org/data/Watt.ntriples",
            "temperature": "http://sw.opencyc.org/2012/05/10/concept/en/DegreeCelsius",
            "volume": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters"
        }

        def format_key(self):
            """
            adds the right full URI to a key
            """
            pass

        def format_value(self):
            """
            adds @type and @value to the value
            """
            pass


class Communication(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['communication'].items():
            setattr(self, k, v)
    pass


class PrimaryPower(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['primary power'].items():
            setattr(self, k, v)
    pass


class Propulsion(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['propulsion'].items():
            setattr(self, k, v)
    pass


class AttitudeAndOrbitControl(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['attitude and orbit control'].items():
            setattr(self, k, v)
    pass


class Thermal(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['thermal'].items():
            setattr(self, k, v)
    pass


class BackupPower(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['backup power'].items():
            setattr(self, k, v)
    pass


class CommandAndData(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['command and data'].items():
            setattr(self, k, v)
    pass


class Detector(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['detector'].items():
            setattr(self, k, v)
    pass


class Structure(SubSystem):
    def __init__(self):
        for k, v in tech_constrains['structure'].items():
            setattr(self, k, v)
    pass