import json

from google.appengine.ext import ndb
from datastore.models import WebResource, Indexer

from handlers.basehandler import JSONBaseHandler


__author__ = 'Lorenzo'


class ArticlesJSONv1(JSONBaseHandler):
    """
    Articles JSON API Handlers.

    Extended from JSONBaseHandler.
    See http://hypermedia.projectchronos.eu/docs
    """

    def __init__(self, *args, **kwargs):
        super(ArticlesJSONv1, self).__init__(*args, **kwargs)
        self._VERSION = 'v04'
        self._BASEPATH = '/articles/' + self._VERSION + '/'

    def get(self, obj=None):
        """
        GET /articles/v04/<name>

        Serve the Articles API.

        :param name: define namespace of the request (getting articles or keywords), can be a void string
        """
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers.add_header("Content-Type", "application/json")

        # if path = / --> Base
        # if path = /by --> ?type or ?keyword
        # if path = /keywords/by ---> ?url

        if self.request.path == self._BASEPATH:
            # serve Articles Base
            setattr(self, '_query_type', 'ALL')
            setattr(self,
                    '_query',
                    self._query.order(-WebResource.published))

            return self.response.out.write(
                json.dumps(
                    self.return_paginated_articles(),
                    indent=2
                )
            )
        elif self.request.path == self._BASEPATH + 'by':
            if self.request.get('type'):
                # serve Articles by type
                if self.request.get('type') in tuple(WebResource.type_of._choices):
                    # set global handler attributes for the handler instance
                    setattr(self, '_query_type', 'TYPE_OF')
                    setattr(self,
                            '_query',
                            self._query.filter(WebResource.type_of == self.request.get('type'))
                                       .order(WebResource.type_of, -WebResource.published))

                    print self._query_type

                    response = self.return_paginated_articles()
                    return self.response.out.write(
                        json.dumps(
                            response,
                            indent=2
                        )
                    )
                else:
                    return self.response.out.write(
                        self.json_error_handler(404, 'incorrect "type" parameter value')
                    )
            elif self.request.get('keyword'):
                # serve articles by keyword
                return self.response.out.write(
                    json.dumps(
                        self.return_articles_by_keyword(self.request.get('keyword')),
                        indent=2
                    )
                )
            else:
                return self.response.out.write(
                    self.json_error_handler(404, 'need to define a ?type or a ?keyword')
                )
        elif self.request.path == self._BASEPATH + 'keywords/by':
            if self.request.get('url'):
                # serve keywords for a given article's url
                response = self.memcache_keywords(self.request.get('url'))
                return self.response.out.write(
                    json.dumps(
                        response,
                        indent=2
                    )
                )
            elif self.request.get('wikislug'):
                # return a mapping between a label from wikipedia and keywords
                pass
            else:
                return self.response.out.write(
                    self.json_error_handler(404, 'need to define a ?url')
                )
        elif self.request.path == self._BASEPATH + 'indexer':
            # return all the terms (keywords) used by the index
            try:
                results = self.memcache_indexer_keywords_distinct()
            except ValueError as e:
                return self.response.out.write(
                    self.json_error_handler(404, 'wrong term')
                )
            return self.response.out.write(
                json.dumps(results)
            )
        elif self.request.path == self._BASEPATH + 'indexer/by':
            if self.request.get('term'):
                # find the genealogy of a term in the Taxonomy
                try:
                    results = self.memcache_indexer_keywords_distinct(self.request.get('term'))
                except ValueError as e:
                    return self.response.out.write(
                        self.json_error_handler(404, 'wrong term')
                    )
                return self.response.out.write(
                    json.dumps(results)
                )
            elif self.request.get('subject'):
                pass
            elif self.request.get('division'):
                pass
            else:
                return self.response.out.write(
                    self.json_error_handler(404, 'need to define a ?term, ?subject or ?division')
                )
        elif self.request.path == self._BASEPATH + 'resources/by':
            if self.request.get('type'):
                # serve keywords for a given type: wikislugs, missions, events ...
                pass
            elif self.request.get('id'):
                # serve a given resource from its id
                pass
            else:
                return self.response.out.write(
                    self.json_error_handler(404, 'need to define a ?url')
                )
        elif isinstance(obj, int):
            # serve a single article object by id
            self.response.set_status(404)
            response = {
                "error": "not implemented",
                "status": "404"
            }
            return self.response.out.write(
                json.dumps(
                    response,
                    indent=2
                )
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

    def return_articles_by_keyword(self, kwd):
        # fetch entities
        webresources = self.memcache_articles_by_keyword(kwd)

        response = {
            "keyword": kwd,
            "articles": [
                w.dump_to_json()
                for w in webresources
            ]
        } if webresources else {"keyword": kwd, "articles_by_keyword": []}

        return response

    def build_response(self, query, bookmark):
        """
        Extends super().build_response
        """
        from config.config import articles_api_version

        # define the right url for the endpoint
        if self._query_type == 'ALL':
            url = articles_api_version(self._API_VERSION) + '?bookmark='
        elif self._query_type == 'TYPE_OF':
            url = articles_api_version(self._API_VERSION) + 'by?type=' +\
                self.request.get('type') + '&bookmark='
        else:
            raise ValueError('JSONBaseHandler.build_response(): self._query_type value error')

        # return the dictionary output
        return {
            'articles': [
                webres.dump_to_json()
                for webres in query
            ],
            'next': url + bookmark if bookmark else None
        }


