import json

from google.appengine.ext import ndb
from datastore.models import WebResource, Indexer

from handlers.basehandler import JSONBaseHandler
from config.config import _PATH, articles_api_version, _MEMCACHE_SLUGS

__author__ = 'Lorenzo'

_VERSION = "04"

_MCACHE_SLUG = "v04_"


class ArticlesJSONv1(JSONBaseHandler):
    """
    Articles JSON API
    See https://github.com/SpaceAppsXploration/rdfendpoints/wiki/Articles-API
    """

    def get(self, name):
        """
        GET /articles/v04/<name>

        Serve the Articles API.

        :param name: define namespace of the request (getting articles or keywords), can be a void string
        """
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers.add_header("Content-Type", "application/json")

        if len(name) == 0 and not self.request.get('url') and not self.request.get('type_of'):
            # serve articles
            setattr(self, '_query_type', 'ALL')
            setattr(self, '_query', self.memcache_webresource_query())
            #print self._query_type
            return self.response.out.write(
                json.dumps(
                    self.return_paginated_articles()
                )
            )
        elif len(name) == 0 and self.request.get('url'):
            # serve keywords for a given article's url
            response = self.memcache_keywords(self.request.get("url"))
            return self.response.out.write(
                json.dumps(response)
            )
        elif isinstance(name, int):
            # serve a single article object by id
            self.response.set_status(404)
            response = {
                "error": "not implemented",
                "status": "404"
            }
            return self.response.out.write(
                json.dumps(response)
            )
        elif name == 'keywords' and self.request.get('keyword'):
            # serve articles by keyword
            return self.response.out.write(
                json.dumps(self.return_articles_by_keyword())
            )
        elif len(name) == 0 and self.request.get('type_of'):
            if self.request.get('type_of') in tuple(WebResource.type_of._choices):
                # set global handler attributes for the handler instance
                setattr(self, '_query_type', 'TYPE_OF')
                setattr(self, '_query', self._query.filter(WebResource.type_of == self.request.get('type_of')).order(WebResource.type_of, -WebResource.published))

                print self._query_type

                response = self.return_paginated_articles()
                return self.response.out.write(
                    json.dumps(response)
                )
            else:
                return self.response.out.write(
                    self.json_error_handler(404, 'incorrect "type_of" parameter value')
                )
        else:
            return self.response.out.write(
                self.json_error_handler(404, 'wrong url')
            )

    def return_paginated_articles(self):
        """
        Fetch and return WebResource paginated query using ndb.query.fetch_page()
        :param query: the query to paginate
        :return: a dict() ready for JSON serialization
        """

        # Forked from https://github.com/GoogleCloudPlatform/appengine-paging-python
        page_size = 25
        cursor = None
        next_bookmark = None
        bookmark = self.request.get('bookmark')
        if bookmark:
            # if bookmark is set, serve the part of the cursor from the given bookamrk plus the page size
            cursor = ndb.Cursor.from_websafe_string(bookmark)

        articles, next_cursor, more = self._query.fetch_page(page_size, start_cursor=cursor)

        # assign the key for the next cursor
        if more:
            next_bookmark = next_cursor.to_websafe_string()

        # serve the data with the link to the next bookmark
        response = self.memcache_articles_pagination(articles, next_bookmark)

        return response

    def return_articles_by_keyword(self):
        # fetch entities
        webresources = self.memcache_articles_by_keyword(self.request.get('keyword'))

        response = {
            "keyword": self.request.get('keyword'),
            "articles_by_keyword": [
                {
                    "article": w.dump_to_json(),
                    "uuid": w.key.id()
                }
                for w in webresources
            ]
        } if webresources else {"keyword": self.request.get('keyword'), "articles_by_keyword": []}

        return response

    def build_response(self, query, bookmark):
        """
        Extends super().build_response
        """
        from config.config import articles_api_version

        if self._query_type == 'ALL':
            url = articles_api_version(self._API_VERSION) + '?bookmark='
        elif self._query_type == 'TYPE_OF':
            url = articles_api_version(self._API_VERSION) + '?type_of=' +\
                self.request.get('type_of') + '&bookmark='
        else:
            raise ValueError('JSONBaseHandler.build_response(): self._query_type value error')

        return {
            'articles': [
                webres.dump_to_json()
                for webres in query
            ],
            'next': url + bookmark if bookmark else None
        }


