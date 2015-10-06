import webapp2
import json
import logging

from google.appengine.api import memcache
from google.appengine.ext import ndb
from datastore.models import WebResource, Indexer

from config.config import _PATH, articles_api_version

__author__ = 'Lorenzo'

_VERSION = "04"

_MCACHE_SLUG = "v04_"


def memcache_webresource_query():
    """
    Get or Set in the memcache the full query of WebResources.
    Updates every six hours (18000 secs)
    :return: Query object or None
    """
    mkey = "WebResource_all"
    if not memcache.get(key=mkey):
        query = WebResource.query()
        memcache.add(key=mkey, value=query, time=18000)
    else:
        query = memcache.get(key=mkey)

    ### by now we exclude media and links children resources (resource with empty title)
    return query.filter(WebResource.title != "").order(WebResource.title, WebResource.key, -WebResource.stored)


def memcache_keywords(url):
    """
    Get or set in the memcache resulting keywords for a given url
    :param url: the url of the WebResource
    :return: a Query object or None
    """
    from urlparse import urlparse
    parts = urlparse(url)
    if parts.scheme and parts.netloc:
        mkey = "Keyword_for_" + url
        if not memcache.get(key=mkey):
            q = WebResource.query().filter(WebResource.url == url).fetch(1)
            results = q[0].get_indexers() if len(q) == 1 else []
            memcache.add(key=mkey, value=results, time=15000)
        else:
            results = memcache.get(key=mkey)
        return results
    else:
        return None


def memcache_articles_pagination(query, bkmark):
    """
    Get or set in the memcache single page for articles
    :param query: the paged query
    :param bkmark: the bookmark's key of the actual page
    :return: dict() with an array of articles and a url to the next bookmarked page
    """
    mkey = "Articles_" + bkmark if bkmark else str("null")
    if not memcache.get(key=mkey):
        listed = {'articles': [webres.dump_to_json()
                               for webres in query],
                  'next': articles_api_version(_VERSION) + '?bookmark=' + bkmark if bkmark else None}
        memcache.add(key=mkey, value=listed, time=15000)
    else:
        listed = memcache.get(key=mkey)
    return listed


def memcache_articles_by_keyword(kwd):
    """
    Get or set in the memcache articles related to a given keyword
    :param kwd: a keyword
    :return: a list
    """
    mkey = "Keywords_" + kwd
    if not memcache.get(key=mkey):
        results = Indexer.get_webresource(kwd)
        memcache.add(key=mkey, value=results)
    else:
        results = memcache.get(key=mkey)

    return results


class ArticlesJSONv1(webapp2.RequestHandler):
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
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'

        if len(name) == 0 and not self.request.get('url'):
            # serve articles
            return self.response.out.write(
                json.dumps(self.return_paginated_articles())
            )
        elif len(name) == 0 and self.request.get('url'):
            # serve keywords for a given article's url
            response = memcache_keywords(self.request.get("url"))
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
        else:
            return self.response.set_status(404)

    def return_paginated_articles(self):
        """
        Fetch and return WebResource paginated query using ndb.query.fetch_page()
        :return:
        """
        query = memcache_webresource_query()

        # Forked from https://github.com/GoogleCloudPlatform/appengine-paging-python
        page_size = 25
        cursor = None
        next_bookmark = None
        bookmark = self.request.get('bookmark')
        if bookmark:
            # if bookmark is set, serve the part of the cursor from the given bookamrk plus the page size
            cursor = ndb.Cursor.from_websafe_string(bookmark)

        articles, next_cursor, more = query.fetch_page(page_size, start_cursor=cursor)

        # assign the key for the next cursor
        if more:
            next_bookmark = next_cursor.to_websafe_string()

        # serve the data with the link to the next bookmark
        response = memcache_articles_pagination(articles, next_bookmark)

        return response

    def return_articles_by_keyword(self):
        # fetch entities
        webresources = memcache_articles_by_keyword(self.request.get('keyword'))

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
