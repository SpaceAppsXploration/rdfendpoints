from __future__ import unicode_literals

__author__ = 'lorenzo'

import os
import time
from bs4 import BeautifulSoup
import feedparser

import webapp2
from google.appengine.ext import ndb

from config.config import _DEBUG

# Adapted from http://tuhrig.de/writing-an-online-scraper-on-google-app-engine-python/


class Item(ndb.Model):
    title = ndb.StringProperty(required=False)
    link = ndb.StringProperty(required=False)
    date = ndb.StringProperty(required=False)


class Scrawler(webapp2.RequestHandler):

    def get(self):
        self.read_feed()
        self.response.out.write(self.print_items())

    def load_links(self):
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

        # print links
        return links

    def read_feed(self):

        feeds = [feedparser.parse(f) for f in self.load_links()]

        for feed in feeds["items"]:
            querry = Item.gql("WHERE link = :1", feed["link"])
            if(querry.count() == 0):
                item = Item()
                item.title = feed["title"]
                item.link = feed["link"]
                item.date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                item.put()

    def print_items(self):
        s = "All items:<br>"
        for item in Item.query():
            s += item.date + " - <a href='" + item.link + "'>" + item.title + "</a><br>"
        return s


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/startcrawling', Scrawler),
], debug=_DEBUG)