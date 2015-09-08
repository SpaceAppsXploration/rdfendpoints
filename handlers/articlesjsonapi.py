import os
import webapp2
import json

from google.appengine.api import memcache
from google.appengine.ext.webapp import template

from config.config import _SERVICE, _PATH

__author__ = 'Lorenzo'


class Articles(webapp2.RequestHandler):
    @staticmethod
    def _memkey(bookmark, keyword):
        '''
        :param bookmark: None or a websafe cursor from NDB
        :param keyword: None or a keyword string from Chronos
        :return: A string key for memcache
        '''
        part0 = bookmark if bookmark else 'frombeginning'
        part1 = keyword if keyword else 'nofilter'
        return 'Articles_{}_{}'.format(part0, part1)

    def get(self):

        if self.request.get("api") and self.request.get("url"):
            # serve keywords for a given article's url
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.headers['Content-Type'] = 'application/json'
            if not memcache.get(key="Keyword_" + self.request.get("url")):
                q = WebResource.query().filter(WebResource.url == self.request.get("url")).fetch(1)
                response = q[0].get_indexers() if len(q) == 1 else []
                memcache.add(key="Keyword_for_" + self.request.get("url"), value=response)
            else:
                response = memcache.get(key="Keyword_for_" + self.request.get("url"))

            return self.response.out.write(
                json.dumps(response)
            )
        else:
            # serve articles
            bookmark = self.request.get('bookmark')
            keyword = self.request.get('keyword')
            mkey = Articles._memkey(bookmark, keyword)
            saved = memcache.get(key=mkey)
            if saved is None:
                articles, more, next_bookmark = Articles._lookup(bookmark, keyword)
                bookmark_parameter = '&bookmark={}'.format(next_bookmark) if next_bookmark else ''
                listed = {'articles': [webres.dump_to_json() for webres in articles],
                          'next': '{}/visualize/articles/?api=true&bookmark={}'.format(_SERVICE, bookmark_parameter)}
                saved = (next_bookmark, listed)
                memcache.add(key=mkey, value=saved)
            else:
                next_bookmark, listed = saved

            if self.request.get("api"):
                # return JSON
                self.response.headers['Access-Control-Allow-Origin'] = '*'
                self.response.headers['Content-Type'] = 'application/json'
                return self.response.out.write(
                    json.dumps(listed)
                )
            # return template
            path = os.path.join(_PATH, 'articles.html')
            return self.response.out.write(template.render(path, {'bookmark': next_bookmark,
                                                                  'articles': listed}))

    @staticmethod
    def _lookup(bookmark, keyword):
        from google.appengine.ext import ndb
        from datastore.models import WebResource, Indexer

        # Forked from https://github.com/GoogleCloudPlatform/appengine-paging-python

        page_size = 25
        cursor = None
        if bookmark:
            cursor = ndb.Cursor.from_websafe_string(bookmark)
        if keyword is not None: # Page through articles with the specified keyword
            refs, next_cursor, more = Indexer.query(ndb.GenericProperty('keyword') == keyword).fetch_page(page_size, start_cursor=cursor)
            articles = ndb.get_multi(ref.webres for ref in refs)
        else:  # Page through all articles
            articles, next_cursor, more = WebResource.query().fetch_page(page_size, start_cursor=cursor)
        next_bookmark = None
        if more:
            next_bookmark = next_cursor.to_websafe_string()
        return articles, more, next_bookmark
