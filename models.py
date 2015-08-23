__author__ = 'lorenzo'

import json
from google.appengine.ext import ndb


class Component(ndb.Model):
    """
    COTS components class
    NOTE: key name or id is a generated hex uuid of the component
    """
    # name of the component instance
    name = ndb.StringProperty()

    # quantities
    minWorkingTemp = ndb.FloatProperty()
    maxWorkingTemp = ndb.FloatProperty()
    hasMonetaryValue = ndb.FloatProperty()
    hasVolume = ndb.FloatProperty()
    hasMass = ndb.FloatProperty()
    hasPower = ndb.FloatProperty()

    # linked @type
    type = ndb.StringProperty()

    # other info
    isStandard = ndb.StringProperty()
    manufacturer = ndb.StringProperty()

    # full jsonld of the component (to find a better solution, may lead to storage/computation overload)
    linked = ndb.JsonProperty(compressed=True)

    @classmethod
    def dump_from_jsonld(cls, jsonld):
        """
        takes a json-ld representing a component and dump it in the datastore.
        Example input: https://github.com/SpaceAppsXploration/RDFvocab/blob/master/raw/COTS_example.json
        :return: datastore instance, put()
        """
        jsonld = json.loads(jsonld)
        m = Component(id=jsonld['uuid'])
        m.linked = jsonld
        for k, v in jsonld.items():
            print k, v
            prop = k.replace('@', '') if k.find('@') != -1 else k[k.rfind('/') + 1:]
            if isinstance(v, dict):
                setattr(m, prop, v['@value'])
            else:
                setattr(m, prop, str(v)) if isinstance(v, unicode) else setattr(m, prop, v)
        print m
        delattr(m, "uuid")
        obj = m.put()
        return obj

    @classmethod
    def parse_to_jsonld(cls, k_id):
        """
        returns the full JSON-LD from the uuid/key name/id
        ENHANCEMENT: needs memcache
        :param k_id: the id
        :return: serialized json
        """
        key = ndb.Key('Component', k_id)
        obj = key.get()
        if not obj:
            raise ValueError('Wrong KEY/ID')
        return json.dumps(obj.linked)





