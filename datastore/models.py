import json
from time import localtime
from datetime import datetime

from google.appengine.ext import ndb

from config.config import articles_api_version

__author__ = 'lorenzo'


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
        results = {'@type': "Collection",
                   '@context': _SERVICE +  "/hydra/contexts/Collection",
                   'members': list()}
        uuid = None
        for q in query:
            print q.key.id(), q.type
            if not uuid:
                uuid = q.type[q.type.rfind('/') + 1:]
            obj = {
                '@context': _SERVICE + "/hydra/context/Component",
                '@id': _SERVICE + "/hydra/spacecraft/components?uuid={}".format(q.key.id()),
                '@type': 'Component',
                'name': q.name
                }
            results['members'].append(obj)
        results['@id'] = _SERVICE + "/hydra/spacecraft/components?uuid={}".format(uuid)
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
        print j
        j = json.loads(j)
        if cls.query().filter(cls.url == j['url']).count() == 0:
            m = WebResource()
            m.title = j['title']
            m.abstract = j['abstract']
            m.url = j['url']
            m.slug = j['keyword']
            obj = m.put()
            index = Indexer(keyword=j['key'], webres=obj)
            index.put()
            return obj

    @classmethod
    def store_feed(cls, entry):
        """
        Store RSS-feed entry coming from feedparser
        """
        if cls.query().filter(cls.url == str(entry['link'])).count() == 0:
            # define the WebResource
            item = WebResource()
            from unidecode import unidecode
            try:
                item.title = unidecode(" ".join(entry['title'].split()))
            except:
                item.title = " ".join(entry['title'].encode('ascii', 'replace').split())

            print item.title
            item.url = str(entry['link'])
            item.stored = datetime(*localtime()[:6])
            item.published = datetime(*entry['published_parsed'][:6]) if 'published_parsed' in entry.keys() else item.stored

            item.abstract = unidecode(" ".join(entry['summary'].strip().encode('ascii', 'replace').split())) if entry['summary'] is not None else ""

            i = item.put()

            try:
                if len(entry.media_content) != 0:
                    print "has media"
                    for obj in entry.media_content:
                        # store image or video as child
                        if cls.query().filter(cls.url == obj.url).count() == 0:
                            m = WebResource(url=obj.url, published=item.published, parent=i.get(), title='', abstract='')
                            m.put()
                            print "media stored"
            except:
                pass

            return i

    @classmethod
    def store_tweet(cls, twt):
        """
        Store a Tweet, its media and its containing link from the Twitter API
        """
        url = 'https://twitter.com/' + str(twt.GetUser().screen_name) + '/status/' + str(twt.GetId())
        try:
            media = twt.media[0]['media_url'] if isinstance(twt.media, list) and len(twt.media) != 0 else None
        except Exception:
            media = twt.media['media_url'] if isinstance(twt.media, dict) and 'media_url' in twt.media.keys() else None
        except:
            media = None

        link = twt.urls[0].expanded_url if len(twt.urls) != 0 else None
        text = twt.text if len(twt.text) > 35 else None
        import time
        published = str(twt._created_at)[:19] + str(twt._created_at)[25:]
        published = time.strptime(published, '%a %b %d %H:%M:%S %Y')
        published = datetime(*published[:6])

        if text:
            if cls.query().filter(cls.url == url).count() == 0:
                # store tweet
                w = WebResource(url=url, published=published, title=str(twt._id), abstract=text)
                k = w.put()
                print "Tweet stored" + str(k)
                if media:
                    if cls.query().filter(cls.url == media).count() == 0:
                        # store image or video as child
                        m = WebResource(url=media, published=published, parent=k, title='', abstract='')
                        m.put()
                        print "media stored"
                if link:
                    if cls.query().filter(cls.url == link).count() == 0:
                        # store contained link as child
                        l = WebResource(url=link, published=published, parent=k, title='', abstract='')
                        l.put()
                        print "link stored"

                return w

    def dump_to_json(self):
        """
        make property values of an instance JSON serializable
        """
        result = {
            "uuid": self.key.id()
        }
        for prop, value in self.to_dict().items():
            # If this is a key, you might want to grab the actual model.
            if prop == 'url':
                result[prop] = value
                result['keywords_url'] = articles_api_version("04") + '?url=' + value
            if isinstance(self, ndb.Model):
                if isinstance(value, datetime):
                    result[prop] = value.isoformat()
                    continue
                elif value is None:
                    result[prop] = None
                    continue
                result[prop] = str(value.encode('ascii', 'replace').strip())

        return result

    def get_indexers(self):
        """
        For a given WebResource, get the keywords stored in Indexer for that resource
        :return: a dict() with a "keywords" property, with value is an array of keyword objects
        """
        query = Indexer.query().filter(Indexer.webres == self.key)
        if query.count() != 0:
            results = {
                "keywords": [
                    {
                        "value": q.keyword,
                        "slug": q.keyword.replace(" ", "+"),
                        "related_urls": articles_api_version("04") + 'keywords?keyword=' + q.keyword
                    }
                    for q in query
                ],
                "url": self.url,
                "uuid": self.key.id()
            }
            return results
        return {
            "keywords": None
        }


class Indexer(ndb.Model):
    """
    A map between keywords and urls
    """
    keyword = ndb.StringProperty()
    webres = ndb.KeyProperty(kind=WebResource)

    @classmethod
    def get_webresource(cls, kwd):
        """
        For a given keyword, get the Web Resources stored in Indexer
        :param kwd: a keyword
        :return: a list of WebResource
        """
        # TO-DO: check if the keyword belong to taxonomy.projectchronos.eu/concept/c
        query = Indexer.query().filter(Indexer.keyword == kwd)
        if query.count() != 0:
            results = [q.webres.get() for q in query]
            return results
        return []


class N3Cache(ndb.Model):
    """
    Cache Dbpedia N3.
    id=url
    """
    # id=url
    n3 = ndb.TextProperty()
    updated = ndb.DateTimeProperty(default=datetime(*localtime()[:6]))

    def check_if_stored(self):
        pass

    def check_if_modified(self):
        pass