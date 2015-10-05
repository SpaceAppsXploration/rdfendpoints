import webapp2
import json

from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

from config.config import _CLIENT_TOKEN

from datastore.models import WebResource, Indexer

from handlers.basehandler import JSONBaseHandler

__author__ = 'Lorenzo'


class DataStoreOperationsAPI(JSONBaseHandler):
    """
    Service handler for operations on crawled resources.

    /datastore/<name> GET:
    - serve a single WebResource object (using ?retrieve= parameter)
    - serve a list of WebResource object's ids (paginated)
    - serve a list of concepts related to a WebResource (using ?retrieve= parameter)

    /datastore/<name> POST:
    #TO-DO: other CRUDs to be implemented
    """
    def get(self, name):
        """
        Handles WebResource
        """
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'

        if self.request.get('token') == _CLIENT_TOKEN:
            if (name == 'webresource' or name == 'indexer') and self.request.get('retrieve'):
                # respond with a single resource of the requested kind
                resource = self.retrieve_a_single_resource(self.request.get('retrieve'), kind=name)
                print type(resource)
                resource = resource.dump_to_json() if resource else None
                return self.response.write(
                    json.dumps(resource)
                ) if resource else self.json_error_handler(404, '?retrieve=ID Wrong ID')
            elif (name == 'webresource' or name == 'indexer') and self.request.get('index'):
                # RETRIEVE a index of WebResource (list of all keys presents in the datastore, paginated)
                from articlesjsonapi import memcache_webresource_query

                query = memcache_webresource_query()

                # Forked from https://github.com/GoogleCloudPlatform/appengine-paging-python
                page_size = 25
                cursor = None
                next_bookmark = None
                bookmark = self.request.get('bookmark')

                if bookmark and bookmark != '':
                    # if bookmark is set, serve the part of the cursor from the given bookamrk plus the page size
                    cursor = ndb.Cursor.from_websafe_string(bookmark)

                articles, next_cursor, more = query.fetch_page(page_size, start_cursor=cursor)

                # assign the key for the next cursor
                if more:
                    next_bookmark = next_cursor.to_websafe_string()

                listed = {'articles': [
                    webres.key.id()
                    for webres in articles
                ],
                'next': next_bookmark if next_bookmark else None}

                return self.response.write(
                    json.dumps(listed)
                )
            elif name == 'concepts' and self.request.get('retrieve'):
                # RETRIEVE keywords related to a WebResource
                from datastore.models import WebResource, Indexer

                # Find concepts related to a WebResource
                resource = self.retrieve_a_single_resource(self.request.get('retrieve'))
                concepts = Indexer.query().filter(Indexer.webres == resource.key)

                listed = {'concepts': [
                    concept.keyword.replace(" ", "+")
                    for concept in concepts
                ],
                'resource_id': resource.key.id()
                }

                return self.response.write(
                    json.dumps(listed)
                )
            else:
                return self.response.write(self.json_error_handler(404))
        else:
            return self.response.write(
                self.json_error_handler(405, exception='Not authorized')
            )

    def post(self, name):
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        if self.request.get('token') == _CLIENT_TOKEN:
            if name == 'webresource':
                from datastore.models import WebResource
                # CREATE WEBRESOURCE
                # UPDATE WEBRESOURCE
                if self.request.get('update') and self.request.get('properties'):
                    res = self.retrieve_a_single_resource(self.request.get('update'))

                    if res:
                        print 'here: ' + str(type(res))
                        props = json.loads(self.request.get('properties'))
                        for prop in props.keys():
                            print prop
                            setattr(res, prop, props[prop])
                        print 'here: ' + str(type(res))
                        res.put()
                        print 'updating properties: ' + str(props)
                else:
                    return self.response.write(
                        self.json_error_handler(
                            404,
                            exception='property \'update\' or \'properties\' missing'
                        )
                    )




            elif name == 'indexer':
                from datastore.models import Indexer
                # CREATE INDEXER
                # UPDATE INDEXER
            else:
                self.response.status = 400
                return json.dumps({"error": 1, "status": 404})

    def retrieve_a_single_resource(self, uuid, kind='webresource'):
        """
        Fetch a single WebResource from a id() or a Key() string
        :param uuid: a key.id() or a Key() string
        :return: a WebResource instance
        """
        # RETRIEVE entity
        models = {
            'webresource': WebResource,
            'indexer': Indexer
        }
        if kind in models.keys():
            try:
                # if the parameter is an id()
                k = ndb.Key(models[kind], int(uuid))
            except ValueError as e:
                try:
                    # if the parameter is a Key()
                    k = ndb.Key(urlsafe=uuid)
                except ProtocolBufferDecodeError as e:
                    return self.response.write(
                        self.json_error_handler(500, exception=repr(e))
                    )

            resource = k.get()
            return resource or None
        else:
            raise ValueError('retrieve_a_single_resource(): Wrong kind')


class Testing(webapp2.RequestHandler):
    """
    /test: test handler
    """
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        try:
            from bs4 import BeautifulSoup
            from json2html import __version__
        except Exception as e:
            raise e
        self.response.write('test passed')

