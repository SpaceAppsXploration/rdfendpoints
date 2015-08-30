from __future__ import unicode_literals

__author__ = 'lorenzo'

import os
from bs4 import BeautifulSoup
import feedparser

import webapp2

from datastore.models import Item
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
        for l in self.load_links():
            self.read_feed(l)

    def load_links(self):
        """
        Loads RSS links from a local file. They are in an XML file with tag <outline/>
        :return:
        """
        #print os.path.dirname(__file__)
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

        #print links
        return links

    def read_feed(self, ln):
        """
        Parse a link with feedparser library. And store the result in the Item() model
        :param ln: a link to a RSS-feed
        :return: None
        """
        feed = feedparser.parse(ln)

        if feed and feed["entries"]:
            for entry in feed["entries"]:
                print entry["link"]
                query = Item.query().filter(Item.link == entry["link"])
                print query.count()
                if query.count() == 0:
                    print entry["link"]
                    try:
                        i = Item.store(entry)
                    except Exception as e:
                        print "Cannot Store: " + str(e) + entry['link']
                        pass
        else:
            print ValueError('No links. Or cannot parse them in: ' + str(feed))
            return None

    def print_items(self):
        """
        utility handler to diplay Item() instances
        :return:
        """
        s = "All items:<br>"
        for item in Item.query():
            s += item.date + " - <a href='" + item.link + "'>" + item.title + "</a><br>"
        return s


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/startcrawling', Scrawler),
], debug=_DEBUG)