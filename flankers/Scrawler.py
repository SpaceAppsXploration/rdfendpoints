from __future__ import unicode_literals

__author__ = 'lorenzo'

import os
from bs4 import BeautifulSoup
import feedparser

import webapp2

from datastore.models import WebResource
from config.config import _DEBUG

# Adapted from http://tuhrig.de/writing-an-online-scraper-on-google-app-engine-python/


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

    def load_links(self):
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

    def read_feed(self, ln):
        """
        Parse a link with feedparser library.
        :param ln: a link to a RSS-feed
        :return: a list of dictionaries containing news from the feed
        """
        feed = feedparser.parse(ln)

        if feed and feed["entries"]:
                return feed["entries"]
        else:
            print ValueError('No links. Or cannot parse them in: ' + str(feed))
            return None

    def store_feeds(self):
        for l in self.load_links():
            entries = self.read_feed(l)
            if entries:
                for entry in entries:
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


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/startcrawling', Scrawler),
], debug=_DEBUG)