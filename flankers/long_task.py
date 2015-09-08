import time
from bs4 import BeautifulSoup
import lib.longtask as longtask
from datastore.models import Indexer, WebResource
from google.appengine.api import memcache

__author__ = 'Lorenzo'


class storeFeeds(longtask.LongRunningTaskHandler):
    def execute_task(self, *args):
        from flankers.Scrawler import Scrawler

        _RSS_FEEDS_CACHE = memcache.get('RSS_FEEDS_CACHE')
        if not _RSS_FEEDS_CACHE or len(_RSS_FEEDS_CACHE) == 0:
            _RSS_FEEDS_CACHE = Scrawler.load_links()
            memcache.set('RSS_FEEDS_CACHE', _RSS_FEEDS_CACHE)
        else:
            _RSS_FEEDS_CACHE = memcache.get('RSS_FEEDS_CACHE')

        print len(_RSS_FEEDS_CACHE)

        l = _RSS_FEEDS_CACHE.pop()
        print l
        entries = Scrawler.read_feed(l)
        if entries:
            for entry in entries:
                # time.sleep(0.1)
                query = WebResource.query().filter(WebResource.url == entry["link"])
                if query.count() == 0:
                    print "STORING: " + entry["link"]
                    try:
                        if 'summary' in entry:
                            s, t = BeautifulSoup(entry['summary'], "lxml"), BeautifulSoup(entry['title'], "lxml")
                            entry['summary'], entry['title'] = s.get_text(), t.get_text()
                        else:
                            t = BeautifulSoup(entry['title'], "lxml")
                            entry['summary'], entry['title'] = None , t.get_text()
                        i = WebResource.store_feed(entry)
                        print "STORED: " + str(i)
                    except Exception as e:
                        print "Cannot Store: " + str(e) + entry['link']
            memcache.set('RSS_FEEDS_CACHE', _RSS_FEEDS_CACHE)
            return None

        memcache.set('RSS_FEEDS_CACHE', _RSS_FEEDS_CACHE)
        print "This Feed has no entries"
        return None


class storeIndexer(longtask.LongRunningTaskHandler):
    def execute_task(self, *args):
        item, key = args
        from flankers.textsemantics import find_related_concepts
        text = item.abstract if len(item.abstract) != 0 else item.title
        labels = find_related_concepts(text)
        for l in labels:
            if Indexer.query().filter(Indexer.webres == key).count() == 0:
                index = Indexer(keyword=l.strip(), webres=key)
                index.put()
                print "indexing stored: " + item.url + ">" + l
