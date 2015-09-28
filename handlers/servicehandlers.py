import webapp2
import json

from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

from config.config import _CLIENT_TOKEN
from handlers.basehandler import JSONBaseHandler

__author__ = 'Lorenzo'


class DataStoreOperationsAPI(JSONBaseHandler):
    """
    /datastore/<name> POST: Service handler for operations on crawled resources
    """
    def get(self, name):
        """
        Handles WebResource
        """
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'

        if self.request.get('token') == _CLIENT_TOKEN:
            if name == 'webresource' and self.request.get('retrieve'):
                from datastore.models import WebResource
                # RETRIEVE WebResource
                try:
                    k = ndb.Key(WebResource, int(self.request.get('retrieve')))
                except ValueError as e:
                    try:
                        k = ndb.Key(urlsafe=self.request.get('retrieve'))
                    except ProtocolBufferDecodeError as e:
                        return self.json_error_handler(500, exception=repr(e))

                resource = WebResource.query().filter(WebResource.key == k).fetch(1)
                resource = resource[0].dump_to_json()
                return self.response.write(
                    resource
                )

            elif name == 'index':
                # RETRIEVE Index (list of all keys presents in the datastore, paginated)
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
            else:
                return self.json_error_handler(404)
        else:
            return self.json_error_handler(405, exception='Not authorized')

    def post(self, name):
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        if self.request.get('token') == _CLIENT_TOKEN:
            if name == 'webresource':
                from datastore.models import WebResource
                # CREATE WEBRESOURCE
                # UPDATE WEBRESOURCE
            elif name == 'indexer':
                from datastore.models import Indexer
                # CREATE INDEXER
                # UPDATE INDEXER
            else:
                self.response.status = 400
                return json.dumps({"error": 1, "status": 404})


class FourOhFour(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(404)


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

