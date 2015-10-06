import urllib
import json
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
            print "STORED: " + str(k)
            return k
        except Exception as e:
            print "Cannot Store: " + str(e)
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
        """
        Take a feed's url from the cached list and fetch posts
        :param args: no arguaments at the moment
        :return: None
        """
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
    """
    Long Task to store tweets
    """
    i = 0

    def recurring(self, timeline):
        for twt in timeline:
            WebResource.store_tweet(twt)
            self.i += 1
        print "Total tweets in list: " + str(self.i)

    def execute_task(self, timeline, remain=list()):
        """
        Store a tweet in the datastore
        Storing method: see WebResource.store_tweet() in models.
        #TO-DO: make this recursive
        :param timeline: a timeline dict() fetched from TW API
        :param remain:
        :return: None
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
    """
    Long Task to handle indexing of a given resource
    """
    def execute_task(self, *args):
        """
        Index an article.
        See Indexer class in models.
        :param args: single object to index and its key
        :return: None
        """
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


class storeFBposts(longtask.LongRunningTaskHandler):
    """
    Long Task to store FB posts
    """
    def execute_task(self, *args):
        """
        Store post, also recursively if response contains paging.
        Storing method: see WebResource.store_fb_post() in models.
        :param args: url of a post and the alias of the page that holds it
        :return: None
        """
        url, alias = args

        def get_wall_recursive(url):
            response = urllib.urlopen(url)
            response = json.loads(response.read())
            if 'error' not in response.keys():
                for o in response['data']:
                    WebResource.store_fb_post(alias, o)
            else:
                from flankers.errors import RESTerror
                raise RESTerror('get_wall_recursive(): FB API error')

            if 'paging' not in response.keys() or not response['paging']['next']:
                return None

            return get_wall_recursive(response['paging']['next'])

        return get_wall_recursive(url)

