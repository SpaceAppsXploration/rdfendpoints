__author__ = 'lorenzo'

import unittest


class CrawlerTest(unittest.TestCase):
    """
    Test for crawling RSS-feeds
    """

    def test_crawl_local(self):
        url = "http://localhost:8080/cron/startcrawling"
        from scripts.remote.remote import get_curling
        res = get_curling(url)
        print res

