__author__ = 'lorenzo'

import unittest
from flankers.Scrawler import Scrawler


class CrawlerTest(unittest.TestCase):
    """
    Test for crawling RSS-feeds. Use the run_test() method.
    """

    class mock_Item():
        """
        A mock class for the Item() model in the datastore
        """
        def __init__(self, t, l, pub, summ):
            from time import time, strptime, gmtime, struct_time
            self.title = str(t)
            self.link = str(l)
            from datetime import datetime
            self.stored = datetime(*gmtime(time())[:6])
            # parsing time.struct_time string into a tuple
            # there is for sure a better way to do it
            result = tuple((int(st.strip().split('=')[1])) for i, st in enumerate(pub[17:-1].split(',')))

            self.published = datetime(*result[:6])
            self.summary = summ

        def store(self):
            return {v: getattr(self, v) for v in dir(self) if not v.startswith('_') and not v == 'store'}

    def test_crawl_local(self):
        url = "http://localhost:8080/cron/startcrawling"
        from scripts.remote.remote import get_curling
        res = get_curling(url)
        print res

    def run_test(self):
        """
        Prints Feed object and multiple attributes if the Item() mock object
        """
        s = Scrawler()
        items = s.load_links()
        print items
        for i in xrange(0, 5):
            try:
                item = s.read_feed(items[i])
            except ValueError:
                continue
            item = self.mock_Item(str(item['title']), str(item['link']), str(item['published_parsed']), str(item['summary'].encode('utf-8')))
            for k, v in item.store().items():
                print k+': ', v

            print "\n"