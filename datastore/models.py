#!/usr/bin/python
# coding=utf-8

__author__ = 'lorenzo'

import json
from time import localtime
from datetime import datetime

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
    holdsSensor = ndb.StringProperty()  # only for collection Spacecraft_Detector, else None

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
        :return: serialized JSON-LD
        """
        key = ndb.Key('Component', k_id)
        obj = key.get()
        if not obj:
            raise ValueError('Wrong KEY/ID')
        return json.dumps(obj.linked, indent=2)

    @classmethod
    def parse_to_json(cls, k_id):
        """
        returns a JSON (implementing HATEOAS)
        https://github.com/SpaceAppsXploration/rdfendpoints/issues/3
        :param k_id: the key id
        :return: serialized JSON
        """
        from config.config import _REST_SERVICE
        key = ndb.Key('Component', k_id)
        obj = key.get()
        if not obj:
            raise ValueError('Wrong KEY/ID')
        j_obj = dict()
        j_obj['ld+json'] = _REST_SERVICE + "%s?format=jsonld" % k_id
        j_obj['uid'] = k_id
        j_obj['collection'] = _REST_SERVICE + obj.type[obj.type.rfind('/')+1:]
        for k, v in obj.to_dict().items():
            if k not in ['linked'] and v:
                j_obj[k] = v
        return json.dumps(j_obj, indent=2)

    @classmethod
    def get_by_collection(cls, collection):
        """
        Get components by subsystem family (Spacecraft_Detector, Spacecraft_Propulsion, etc. )
        :param collection: standard string for a subsystem, see flankers.tools.families
        :return: a Query object
        """
        target = "http://ontology.projectchronos.eu/subsystems/%s" % collection
        query = Component.query(Component.type == target)
        if not query:
            raise ValueError('Wrong collection name')
        return query

    @classmethod
    def restify(cls, query):
        """
        Dumps into JSON for REST a Component.query()
        :param query: a Query object
        :return: a formatted and dumped JSON
        """
        from config.config import _REST_SERVICE
        results = list()
        for q in query:
            print q.key.id(), q.type
            obj = {'id': q.key.id(),
                   'name': q.name,
                   'application/ld+json': _REST_SERVICE + "%s?format=jsonld" % q.key.id(),
                   'go_to_json': _REST_SERVICE + q.key.id(),
                   'type': {
                       'application/ld+json': q.type,
                       'go_to_collection': _REST_SERVICE + q.type[q.type.rfind('/')+1:]
                   }
            }
            results.append(obj)
        return json.dumps(results, indent=2)

    @classmethod
    def hydrafy(cls, query):
        """
        Dumps into a JSON-LD for HYDRA a Component.query()
        :param query: a Query object
        :return: a formatted JSON-LD
        """
        from config.config import _SERVICE
        results = list()
        for q in query:
            print q.key.id(), q.type
            obj = {
                '@context': _SERVICE + "/hydra/context/Component",
                '@id': _SERVICE + "/hypermedia/spacecraft/components?uuid={}".format(q.key.id()),
                '@type': 'Component',
                'name': q.name
                }
            results.append(obj)
        return json.dumps(results, indent=2)


class WebResource(ndb.Model):
    """
    Indexed Web pages and single entries of a crawled RSS-feed
    """
    title = ndb.StringProperty()
    abstract = ndb.TextProperty()
    url = ndb.StringProperty()
    stored = ndb.DateTimeProperty(default=datetime(*localtime()[:6]))
    published = ndb.DateTimeProperty(default=None)

    @classmethod
    def dump_from_json(cls, j):
        """
        Store a WebResource from a JSON object
        :param j: a JSON
        :return: a WebResource
        """
        print j.decode('utf-8')
        try:
            j = json.loads(j)
            m = WebResource()
            m.title = j['title']
            m.abstract = j['abstract']
            m.url = j['url']
            m.slug = j['keyword']
            obj = m.put()
            index = Indexer(keyword=j['key'], webres=obj)
            index.put()
        except Exception as e:
            raise Exception('Error in WeResource storage', e)
        return obj

    @classmethod
    def store_feed(cls, entry):
        """
        Store RSS-feed entry coming from Scrawler, and related index entries
        """
        # define the WebResource
        item = WebResource()
        item.title = " ".join(entry['title'].encode('ascii', 'ignore').split())
        print item.title
        item.url = str(entry['link'])
        item.stored = datetime(*localtime()[:6])
        item.published = datetime(*entry['published_parsed'][:6]) if 'published_parsed' in entry.keys() else item.stored

        item.abstract = ' '.join(entry['summary'].strip().encode('ascii', 'ignore').split()) if entry['summary'] is not None else ''
        i = item.put()

        # create the Index entries
        from flankers.textsemantics import find_related_concepts
        text = item.abstract if entry['summary'] is not None else item.title
        labels = find_related_concepts(text)
        for l in labels:
            print l
            index = Indexer(keyword=l.strip(), webres=i)
            index.put()
        return i

    def dump_to_json(self):
        """
        make property values of an instance JSON serializable
        """
        result = {}
        for prop, value in self.to_dict().items():
            # If this is a key, you might want to grab the actual model.
            if isinstance(self, ndb.Model):
                result[prop] = str(value)

        return result


class Indexer(ndb.Model):
    keyword = ndb.StringProperty()
    webres = ndb.KeyProperty(kind=WebResource)