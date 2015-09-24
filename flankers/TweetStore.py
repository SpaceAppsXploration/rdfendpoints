import webapp2
import twitter

from google.appengine.api import memcache

from config.config import _DEBUG
from config.tw_secret import token, token_key, con_secret, con_secret_key

__author__ = 'Lorenzo'


class TweetStore(webapp2.RequestHandler):
    """
    A very basic fetch and store for tweets
    """
    api = twitter.Api(consumer_key=con_secret,
                      consumer_secret=con_secret_key,
                      access_token_key=token,
                      access_token_secret=token_key,
                      cache=None)

    def get(self):
        """
        Handler for the cronjob: /cron/storetweets
        :return:
        """
        #self.test_twitter()

        timeline = self.list_timeline(self.load_list_from_memcache())
        self.store_tweets(timeline)

    def lists_ids(self):
        """
        Return id and slug of the lists
        :return: a list() of tuple(id, slug)
        """
        twitter_lists = self.api.GetLists(screen_name='XplorationApp')
        return [(l.__dict__['_id'], l.__dict__['_name']) for l in twitter_lists]

    def load_list_from_memcache(self):
        """
        Pop an element from lists' cache, reload lists cache if empty
        :return: a tuple(id, slug) of a list
        """

        TW_LISTS_CACHE = memcache.get('TW_LISTS_CACHE')
        if not TW_LISTS_CACHE or len(TW_LISTS_CACHE) == 0:
            TW_LISTS_CACHE = self.lists_ids()
            memcache.set('TW_LISTS_CACHE', TW_LISTS_CACHE)

        listed = TW_LISTS_CACHE.pop(0)
        print len(TW_LISTS_CACHE)

        memcache.set('TW_LISTS_CACHE', TW_LISTS_CACHE)
        return listed

    def list_timeline(self, targs):
        """
        Return the timeline for a given list
        :param targs: a tuple(id, slug) of a list
        :return: a list() of Tweets objects
        """
        _id, _slug = targs[0], targs[1]
        pub_list = self.api.GetListTimeline(list_id=_id, slug=_slug)
        return pub_list

    def store_tweets(self, tmline):
        from flankers.long_task import storeTweets
        s = storeTweets()
        s.execute_task(tmline)

    def test_twitter(self):
        pass


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/storetweets', TweetStore),
], debug=_DEBUG)
