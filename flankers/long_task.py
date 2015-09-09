import time
from bs4 import BeautifulSoup
import lib.longtask as longtask
from datastore.models import Indexer, WebResource
from google.appengine.api import memcache

__author__ = 'Lorenzo'


def store_feed(e):
    """
    store a single entry from the feedparser
    :param e: the entry
    :return: if succeed the stored key else None
    """
    query = WebResource.query().filter(WebResource.url == e["link"])
    if query.count() == 0:
        print "STORING: " + e["link"]
        try:
            if 'summary' in e:
                s, t = BeautifulSoup(e['summary'], "lxml"), BeautifulSoup(e['title'], "lxml")
                e['summary'], e['title'] = s.get_text(), t.get_text()
            else:
                t = BeautifulSoup(e['title'], "lxml")
                e['summary'], e['title'] = None , t.get_text()
            k = WebResource.store_feed(e)
            print "STORED: " + str(k.key)
            return k
        except Exception as e:
            print "Cannot Store: " + str(e) + e['link']
            return None
    else:
        print "Resource already stored"
        return None


class storeFeeds(longtask.LongRunningTaskHandler):
    """
    Handle the long task for storing feeds.
    #TO-DO: move memcache in handler Scrawler
    """
    def execute_task(self, *args):
        from flankers.scrawler import Scrawler

        RSS_FEEDS_CACHE = memcache.get('RSS_FEEDS_CACHE')
        if not RSS_FEEDS_CACHE or len(RSS_FEEDS_CACHE) == 0:
            RSS_FEEDS_CACHE = Scrawler.load_links()
            memcache.set('RSS_FEEDS_CACHE', RSS_FEEDS_CACHE)

        print len(RSS_FEEDS_CACHE)

        l = RSS_FEEDS_CACHE.pop()
        print l
        entries = Scrawler.read_feed(l)
        if entries:
            for entry in entries:
                #
                # Store feed
                #
                store_feed(entry)
            memcache.set('RSS_FEEDS_CACHE', RSS_FEEDS_CACHE)
            return None

        memcache.set('RSS_FEEDS_CACHE', RSS_FEEDS_CACHE)
        print "This Feed has no entries"
        return None


class storeTweets(longtask.LongRunningTaskHandler):
    i = 0

    def recurring(self, timeline):
        for twt in timeline:
            WebResource.store_tweet(twt)
            self.i += 1
        print "Total tweets in list: " + str(self.i)

    def execute_task(self, timeline, remain=list()):
        """
        #TO-DO: make this recursive
        :param timeline:
        :param remain:
        :return:
        """
        for twt in timeline:
            if isinstance(twt, list):
                print "twt is a list"
                self.recurring(twt)
            else:
                WebResource.store_tweet(twt)
                self.i += 1
        print "Total tweets: " + str(self.i)


class storeIndexer(longtask.LongRunningTaskHandler):
    def execute_task(self, *args):
        item, key = args
        from flankers.textsemantics import find_related_concepts
        if not (item.title == '' and item.abstract == ''):
            # if item is not a media or a link from Twitter
            # it is or a feed or a tweet
            text = item.abstract if len(item.abstract) != 0 else item.title
            labels = find_related_concepts(text)
            for l in labels:
                if Indexer.query().filter(Indexer.webres == key).count() == 0:
                    index = Indexer(keyword=l.strip(), webres=key)
                    index.put()
                    print "indexing stored: " + item.url + ">" + l

