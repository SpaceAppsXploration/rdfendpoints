__author__ = 'lorenzo'

from google.appengine.ext import ndb


class Component(ndb.Model):
    """
    COTS components class
    """
    # generated uuid of the component
    label = ndb.StringProperty()
    # name of the component instance
    name = ndb.StringProperty()

    minWorkingTemp = ndb.FloatProperty()
    maxWorkingTemp = ndb.FloatProperty()
    hasMonetaryValue = ndb.FloatProperty()
    hasVolume = ndb.FloatProperty()
    hasMass = ndb.FloatProperty()
    hasPower = ndb.FloatProperty()

    function = ndb.StringProperty()
    isStandard = ndb.StringProperty()
    manufacturer = ndb.StringProperty()

    @classmethod
    def dump_from_jsonld(cls, jsonld):
        """
        takes a json-ld representing a component and dump it in the datastore.
        Example input: https://github.com/SpaceAppsXploration/RDFvocab/blob/master/raw/COTS_example.json
        :return: datastore instance, Model.put()
        """
        pass





