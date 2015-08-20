__author__ = 'lorenzo'

import random
import uuid

from generator import generate_object


class SubSystem(object):

    name = None

    def __init__(self, attrs):
        """
        Factory for subsystems components
        :param attrs: a dictionary with the instance attributes
        """
        for k, v in attrs.items():
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
        Checks if an attribute in the class or a value is a constraints
        :param attr: the class attribute
        :return: bool
        """
        if isinstance(attr, dict) and all(k in attr.keys() for k in ['min', 'max']):
            return True
        return False

    @classmethod
    def generate_py_instance(cls, kind, specs):
        """
        Take the technical specs of a family of subsystems (communication, propulsion, ...) and create components objects
        :param kind: string representing the kind/family
        :param specs: dictionary of specs taken from constraints
        :return: component as Python object
        """
        name = str(random.randrange(0, 200)) + str(random.choice(['T', 'W', 'KV', 'JFG', 'WNT', 'SD'])) + ' ' + kind
        json_obj = {'id': uuid.uuid4().hex, 'name': name}
        json_obj = dict(json_obj.items() + generate_object(kind, specs).items())
        classname = SubSystem.stringify(json_obj['kind'])
        obj = type(classname, (SubSystem,), json_obj)
        return obj

    @classmethod
    def generate_jsonld(cls, component):
        """
        Tools for converting a JSON object taken from  generate_instances() to a compacted JSON-LD
        UNDER CONSTRUCTION
        see RDFvocab/raw/COTS_example.json for an example of outcome
        :param component: JSON object as dict
        :return: JSON-LD object as dict
        """
        if not issubclass(component, SubSystem):
            raise ValueError

        result = {
            "@id": "http://ontology.projectchronos.eu/COTS/" + component.id,
            "@type": component.linked,
            "http://ontology.projectchronos.eu/subsystems/name": component.name,
            "http://ontology.projectchronos.eu/subsystems/manufacturer": "Chronos",
            "http://ontology.projectchronos.eu/subsystems/isStandard": "Cubesat",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#label": "e3349c8fe32d4174a405aeee1e441fad",
        }

        units = {
            "vocabs": "http://ontology.projectchronos.eu/",
            "subsystems:hasMass": "http://sw.opencyc.org/2012/05/10/concept/en/Gram",
            "subsystems:hasMonetaryValue": "http://sw.opencyc.org/2012/05/10/concept/en/Euro",
            "subsystems:hasPower": "http://dbpedia.org/data/Watt.ntriples",
            "temperature": "http://sw.opencyc.org/2012/05/10/concept/en/DegreeCelsius",
            "subsystems:hasVolume": "http://ontology.projectchronos.eu/subsystems/cubicMillimeters"
        }

        def format_key(key):
            """
            Gives the right full URI to a key
            :param key: a string, a dictionary key
            :return: the right key for the JSON-LD
            """
            if key.find(':') != -1:
                # if key is a vocabulary property
                subs = key.split(':')
                # format the key as a linked data property
                new_key = units['vocabs'] + subs[0] + '/' + subs[1]
                return new_key
            else:
                raise ValueError('input is not a vocabulary KEY from a component dictionary')

        def format_value(key, value):
            """
            adds @type and @value to the value
            """
            try:
                # look for quantitative values
                if all(i(value) for i in (int, long, float, complex)):
                    return {
                        "@type": units[key] if 'Temp' not in key else units['temperature'],
                        "@value": value
                    }
            except ValueError:
                # if the value is a link or string
                if key.find(':') != -1:
                    subs = key.split(':')
                    new_value = units['vocabs'] + subs[0] + '/' + value
                    return new_value
                else:
                    raise ValueError('input is not a quantitative VALUE or an object property from a component dictionary')

        for k, v in component.__dict__.items():
            if v is not None:
                try:
                    print k, v
                    result[format_key(k)] = format_value(k, v)
                except ValueError as e:
                    # print e
                    pass

        return result


class Communication(SubSystem):
    def __init__(self, attrs):
        self.name = 'communication'
        super(Communication, self).__init__(attrs=attrs)
    pass


class PrimaryPower(SubSystem):
    def __init__(self, attrs):
        self.name = 'primary power'
        super(PrimaryPower, self).__init__(attrs)
    pass


class Propulsion(SubSystem):
    def __init__(self, attrs):
        self.name = 'propulsion'
        super(Propulsion, self).__init__(attrs)
    pass


class AttitudeAndOrbitControl(SubSystem):
    def __init__(self, attrs):
        self.name = 'attitude and orbit control'
        super(AttitudeAndOrbitControl, self).__init__(attrs)
    pass


class Thermal(SubSystem):
    def __init__(self, attrs):
        self.name = 'thermal'
        super(Thermal, self).__init__(attrs)
    pass


class BackupPower(SubSystem):
    def __init__(self, attrs):
        self.name = 'backup power'
        super(BackupPower, self).__init__(attrs)
    pass


class CommandAndData(SubSystem):
    def __init__(self, attrs):
        self.name = 'command and data'
        super(CommandAndData, self).__init__(attrs)
    pass


class Detector(SubSystem):
    def __init__(self, attrs):
        self.name = 'detector'
        super(Detector, self).__init__(attrs)
    pass


class Structure(SubSystem):
    def __init__(self, attrs):
        self.name = 'structure'
        super(Structure, self).__init__(attrs)
    pass