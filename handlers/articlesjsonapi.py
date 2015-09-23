import os
import webapp2
import json
import logging

from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from datastore.models import WebResource, Indexer

from config.config import _PATH, articles_api_version

__author__ = 'Lorenzo'

_VERSION = "04"


class Articles(webapp2.RequestHandler):
    """
    Serve the Articles API
    GET /articles/?
    :param api: if set to true serves JSON
    :param bookmark: holds the key for pagination
    :param url: if present serves the keywords related to a url
    :param keyword: if present serves articles by keyword
    """
    def get(self):


        self.response.headers['Access-Control-Allow-Origin'] = '*'

        if self.request.get("url"):
            # serve keywords for a given article's url
            self.response.headers['Content-Type'] = 'application/json'
            response = memcache_keywords(self.request.get("url"))
            return self.response.out.write(
                json.dumps(response)
            )
        elif self.request.get("keyword"):
            pass
        else:
            # serve articles
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
            listed = memcache_articles_pagination(articles, next_bookmark)

            if self.request.get("api") == 'true':
                # param 'api' is true, return JSON
                self.response.headers['Content-Type'] = 'application/json'
                return self.response.out.write(
                    json.dumps(listed)
                )
            # param 'api' is not set or false, return template
            path = os.path.join(_PATH, 'articles.html')
            return self.response.out.write(template.render(path, {'bookmark': next_bookmark,
                                                                  'articles': listed}))


def memcache_webresource_query():
    """
    Get or Set in the memcache the full query of WebResources.
    Updates every six hours (18000 secs)
    :return: Query object or None
    """
    if not memcache.get(key="WebResource_all"):
        query = WebResource.query()
        memcache.add(key="WebResource_all", value=query, time=18000)
    else:
        query = memcache.get(key="WebResource_all")
    return query


def memcache_keywords(url):
    """
    Get or set in the memcache resulting keywords for a given url
    :param url: the url of the WebResource
    :return: a Query object or None
    """
    from urlparse import urlparse
    parts = urlparse(url)
    if parts.scheme and parts.netloc:
        if not memcache.get(key="Keyword_" + url):
            q = WebResource.query().filter(WebResource.url == url).fetch(1)
            results = q[0].get_indexers() if len(q) == 1 else []
            memcache.add(key="Keyword_for_" + url, value=results, time=15000)
        else:
            results = memcache.get(key="Keyword_for_" + url)
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


class ArticlesJSONv1(webapp2.RequestHandler):
    def get(self, name):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'

        if len(name) == 0 and not self.request.get('url'):
            # serve articles
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
            listed = memcache_articles_pagination(articles, next_bookmark)

            return self.response.out.write(
                json.dumps(listed)
            )
        elif len(name) == 0 and self.request.get('url'):
            # serve keywords for a given article's url
            self.response.headers['Content-Type'] = 'application/json'
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

            # TO-DO: implement memcache
            webresources = Indexer.get_webresource(self.request.get('keyword'))
            response = [
                {
                    "article": w.dump_to_json(),
                    "uuid": w.key.id()
                }
                for w in webresources
            ]
            return self.response.out.write(
                json.dumps(response)
            )
        else:
            return self.response.set_status(404)
