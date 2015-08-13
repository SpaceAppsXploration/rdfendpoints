__author__ = 'lorenzo'

import random
import uuid

from constraints import tech_constrains  # technical constraints in constraints.py
from generator import generate_object


class SubSystem(object):

    name = None

    def __init__(self):
        for k, v in tech_constrains[self.name].items():
            setattr(self, k, v)

    @classmethod
    def stringify(cls, name):
        """
        natural language to camelCase
        :param name: str
        :return: str
        """
        return name.title().replace(" ", "")

    @classmethod
    def naturify(cls, slug):
        """
        inverse of stringify
        :param slug: str
        :return: str
        """
        import re
        s = re.sub(r"([A-Z])", r" \1", slug).split()
        return " ".join(s).lower()

    @classmethod
    def is_constraint(cls, attr):
        """
        Checks if an attribute in the class is a constraints
        :param attr: the class attribute
        :return: bool
        """
        if isinstance(attr, dict) and all(k in attr.keys() for k in ['min', 'max']):
            return True
        return False

    @classmethod
    def generate_instance(cls, kind, specs):
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
        if not isinstance(component, dict):
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

        return component


class Communication(SubSystem):
    def __init__(self):
        self.name = 'communication'
        super(Communication, self).__init__()
    pass


class PrimaryPower(SubSystem):
    def __init__(self):
        self.name = 'primary power'
        super(PrimaryPower, self).__init__()
    pass


class Propulsion(SubSystem):
    def __init__(self):
        self.name = 'propulsion'
        super(Propulsion, self).__init__()
    pass


class AttitudeAndOrbitControl(SubSystem):
    def __init__(self):
        self.name = 'attitude and orbit control'
        super(AttitudeAndOrbitControl, self).__init__()
    pass


class Thermal(SubSystem):
    def __init__(self):
        self.name = 'thermal'
        super(Thermal, self).__init__()
    pass


class BackupPower(SubSystem):
    def __init__(self):
        self.name = 'backup power'
        super(BackupPower, self).__init__()
    pass


class CommandAndData(SubSystem):
    def __init__(self):
        self.name = 'command and data'
        super(CommandAndData, self).__init__()
    pass


class Detector(SubSystem):
    def __init__(self):
        self.name = 'detector'
        super(Detector, self).__init__()
    pass


class Structure(SubSystem):
    def __init__(self):
        self.name = 'structure'
        super(Structure, self).__init__()
    pass