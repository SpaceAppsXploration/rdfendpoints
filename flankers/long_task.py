import time
from bs4 import BeautifulSoup
import lib.longtask as longtask
from datastore.models import Indexer, WebResource

__author__ = 'Lorenzo'


class storeFeeds(longtask.LongRunningTaskHandler):
    def execute_task(self, *args):
        from flankers.Scrawler import Scrawler
        for l in Scrawler.load_links():
            entries = Scrawler.read_feed(l)
            if entries:
                for entry in entries:
                    time.sleep(0.5)
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


class storeIndexer(longtask.LongRunningTaskHandler):
    def execute_task(self, *args):
        item, key = args
        from flankers.textsemantics import find_related_concepts
        text = item.abstract if len(item.abstract) != 0 else item.title
        labels = find_related_concepts(text)
        for l in labels:
            index = Indexer(keyword=l.strip(), webres=key)
            index.put()
            print "indexing stored: " + item.url + ">" + l
