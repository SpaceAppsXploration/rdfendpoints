import webapp2
import datetime
from time import localtime

from config.config import _DEBUG
from datastore.models import WebResource
from google.appengine.api import memcache

__author__ = 'Lorenzo'

from datastore.models import Indexer

class Indexing(webapp2.RequestHandler):
    """
    A very basic crawler for RSS links
    #TO-DO: implement memecache for stored items not yet indexed
    """

    def __init__(self, *args, **kwargs):
        super(Indexing, self).__init__(*args, **kwargs)
        self.mkey = "INDEXING_QUEUE"

    def get(self):
        """
        Handler for the cronjob: /cron/indexing
        It store keywords indexing of the most recent WebResource stored
        :return:
        """
        # create the Index entries
        from flankers.long_task import storeIndexer

        if not memcache.get(key=self.mkey):
            an_hour = datetime.datetime(*localtime()[:6]) - datetime.timedelta(hours=2)
            print an_hour
            query = WebResource.query().filter(WebResource.stored > an_hour)
            if query.count() == 0:
                memcache.delete(key=self.mkey)
                return None
            print "queried: " + str(query.count())

            listed = []
            for k in query.iter(keys_only=True):
                listed.append(k)

            memcache.add(key=self.mkey, value=listed)
            to_index = listed
        else:
            to_index = memcache.get(key=self.mkey)

        print "To be indexed: " + str(len(to_index))

        if len(to_index) != 0:
            key = to_index.pop()
            print "popped", str(len(to_index))
            print "popping", str(key)

            try:
                s = storeIndexer()
                s.execute_task(key.get(), key)
                del s
            except Exception:
                print "resource already indexed"
                pass

            memcache.set(key=self.mkey, value=to_index)
        else:
            memcache.delete(key=self.mkey)
            print "nothing to index"




application = webapp2.WSGIApplication([
    webapp2.Route('/cron/indexing', Indexing),
], debug=_DEBUG)

