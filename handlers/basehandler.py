"""
All the Base Handlers needed by the server
"""

import webapp2
import json

from config.config import _PATH
from google.appengine.api import memcache

__author__ = 'Lorenzo'

from config.config import _MEMCACHE_SLUGS  # holds the different keys used in the memcache
from datastore.models import WebResource, Indexer


class JSONBaseHandler(webapp2.RequestHandler):
    """
    Handler For JSON Endpoints.

    Extends RequestHandler with new custom methods for:
    - Error Handling
    - Handling different queries with the same handler
    - Implement memcache for the operations in the handler
    """

    def __init__(self, *args, **kwargs):
        super(JSONBaseHandler, self).__init__(*args, **kwargs)
        self._query = self.memcache_webresource_query()  # holds the query needed to serve the data
        self._query_type = None  # type of the query: ALL=global TYPE_OF=filtered by type ...
        self._API_VERSION = '04'

    def json_error_handler(self, code, exception=None):
        """
        Print out error in JSON as a readable dictionary.

        :param code: status code to display (int)
        :param exception: error message
        :return: a dict()
        """
        self.response.status = code
        return json.dumps(
            {"error": 1, "status": code}
        ) if not exception else json.dumps(
            {"error": 1, "status": code, "exception": exception}
        )

    def memcache_webresource_query(self):
        """
        Get or Set in the memcache the full query of WebResources.

        It's used by all the endpoints to fetch all the data.
        Updates every six hours (18000 secs)
        :return: Query object or None
        """
        mkey = _MEMCACHE_SLUGS['ALL']
        if not memcache.get(key=mkey):
            self._query = WebResource.query()
            memcache.add(key=mkey, value=self._query, time=18000)
        else:
            self._query = memcache.get(key=mkey)

        ### Note for filtering: http://stackoverflow.com/a/28627068/2536357
        return self._query

    def memcache_keywords(self, url):
        """
        Get or set in the memcache resulting keywords for a given url.

        GET /articles/<version>/?url=<resource url>
        :param url: the url of the WebResource
        :return: a Query object or None
        """
        from urlparse import urlparse
        parts = urlparse(url)
        if parts.scheme and parts.netloc:
            mkey = _MEMCACHE_SLUGS['KEYWORDS'] + url
            if not memcache.get(key=mkey):
                q = self._query.filter(WebResource.url == url).fetch(1)
                results = q[0].get_indexers() if len(q) == 1 else []
                memcache.add(key=mkey, value=results, time=15000)
            else:
                results = memcache.get(key=mkey)
            return results
        else:
            return None

    def memcache_articles_pagination(self, query, bkmark):
        """
        Get or set in the memcache single page for articles.

        Store different keys based on cursor bookmarks. If the requested data is not in
        the cache, build the response (build_response) and cache it
        :param query: the paged query
        :param bkmark: the bookmark's key of the actual page
        :return: dict(), see build_response()
        """
        mkey = self._query_type + bkmark if bkmark else str("null")
        if not memcache.get(key=mkey):
            listed = self.build_response(query, bkmark)
            memcache.add(key=mkey, value=listed, time=15000)
        else:
            listed = memcache.get(key=mkey)
        return listed

    def memcache_articles_by_keyword(self, kwd):
        """
        Get or set in the memcache articles related to a given keyword.

        GET /articles/<version>/?keyword=<some keyword>
        :param kwd: a keyword
        :return: a list
        """
        mkey = _MEMCACHE_SLUGS['KWD_BY_ARTICLE'] + kwd
        if not memcache.get(key=mkey):
            results = Indexer.get_webresource(kwd)
            memcache.add(key=mkey, value=results)
        else:
            results = memcache.get(key=mkey)

        return results

    def memcache_indexer_keywords_distinct(self):
        """
        Get or set in the memcache the keywords indexed with count.

        :return: a Query()
        """
        mkey = _MEMCACHE_SLUGS['INDEXER_DISTINCT']
        if not memcache.get(key=mkey):
            query = Indexer.query(projection=[Indexer.keyword], distinct=True)
            results = {
                "indexed": [
                    {
                        "keyword": q.keyword,
                        "count": Indexer.query(Indexer.keyword == q.keyword).count()
                    }
                    for q in query
                ],
                "n_indexed": query.count()
            }
            memcache.add(key=mkey, value=results)
        else:
            results = memcache.get(key=mkey)

        return results

    def build_response(self, query, bookmark):
        """
        To be extended in the handler
        :param query: a Query or a Cursor
        :param bookmark: a cursor's bookamrk or None
        """
        pass


class BaseHandler(webapp2.RequestHandler):
    """def handle_exception(self, exception, debug):
        import os
        from google.appengine.ext.webapp import template
        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)

        path = os.path.join(_PATH, 'over_quota.html')
        return self.response.out.write(template.render(path, {}))
    """
    pass
