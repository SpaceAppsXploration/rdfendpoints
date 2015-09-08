from __future__ import unicode_literals

__author__ = 'lorenzo'

import os
from bs4 import BeautifulSoup
import feedparser

import webapp2

from config.config import _DEBUG


class Scrawler(webapp2.RequestHandler):
    """
    A very basic crawler for RSS links
    """
    def get(self):
        """
        Handler for the cronjob: /cron/startcrawling
        :return:
        """
        self.store_feeds()

    @staticmethod
    def load_links():
        """
        Loads RSS links from a local file. They are in an XML file with tag <outline/>
        :return: A list of URLs of RSS-feeds
        """

        feeds_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'files', 'newsfox.xml')
        with open(feeds_file) as f:
            markup = f.read()
        body = BeautifulSoup(markup, "lxml-xml").body
        outlines = body.find_all('outline')
        links = []
        for o in outlines:
            try:
                links.append(str(o['xmlUrl']))
            except KeyError as e:
                pass
            except Exception as e:
                raise e
        return links

    @staticmethod
    def read_feed(ln):
        """
        Parse a link with feedparser library.
        :param ln: a link to a RSS-feed
        :return: a list of dictionaries containing news from the feed
        """
        feed = feedparser.parse(ln)

        if feed and feed["entries"]:
            return feed["entries"]
        else:
            print ValueError('No links. Or cannot parse them in: ' + str(ln))
            return None

    @staticmethod
    def store_feeds():
        """
        Use long task class to store feeds
        :return:
        """
        from flankers.long_task import storeFeeds
        s = storeFeeds()
        s.execute_task()


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/startcrawling', Scrawler),
], debug=_DEBUG)