import os
import webapp2
import json

from google.appengine.api import memcache
from google.appengine.ext.webapp import template

from config.config import _SERVICE, _PATH

__author__ = 'Lorenzo'


class Articles(webapp2.RequestHandler):
    def get(self):
        from google.appengine.ext import ndb
        from datastore.models import WebResource

        # Forked from https://github.com/GoogleCloudPlatform/appengine-paging-python

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
            if not memcache.get(key="WebResource_all"):
                query = WebResource.query()
                memcache.add(key="WebResource_all", value=query)
            else:
                query = memcache.get(key="WebResource_all")

            page_size = 25
            cursor = None
            bookmark = self.request.get('bookmark')
            if bookmark:
                cursor = ndb.Cursor.from_websafe_string(bookmark)

            articles, next_cursor, more = query.fetch_page(page_size, start_cursor=cursor)

            next_bookmark = None
            if more:
                next_bookmark = next_cursor.to_websafe_string()
            print next_bookmark

            mkey = "Articles_" + next_bookmark
            if not memcache.get(key=mkey):
                listed = {'articles': [webres.dump_to_json() for webres in articles], 'next': _SERVICE + '/visualize/articles/?api=true&bookmark=' + next_bookmark}
                memcache.add(key=mkey, value=listed)
            else:
                listed = memcache.get(key=mkey)

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
