__author__ = 'lorenzo'

import os
import signal
import time
from bs4 import BeautifulSoup
from microblogcrawler.crawler import FeedCrawler


class MyFeedCrawler(FeedCrawler):
    """ A basic testing class implementation. """

    results = []

    def __init__(self, links, start_now=False):
        self.total_time = 0
        self.count = 0
        FeedCrawler.__init__(self, links, start_now=start_now)

    def on_start(self):
        self.count = 0
        self.total_time = time.time()

    def on_finish(self):
        print '{0} New Items | {1} seconds'.format(self.count, time.time() - self.total_time)
        print self.results[0:5]  # only the first 5 items crawled are printed
        self.stop(now=True)

    def on_item(self, link, info, item):
        self.count += 1
        print "CRAWLING: " + link
        #print 'Item text: {0}\n{1}'.format(info, item)
        self.results.append({
            "info": info,
            "item": item
        })
        pass

    def on_error(self, link, error):
        print 'Error for {}:\n {}'.format(link, error['description'])
        pass

#print os.path.dirname(__file__)
feeds_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'files', 'newsfox.xml')

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
if __name__ == '__main__':
    # freeze_support()
    MyFeedCrawler.ALLOW_RSS = True

    crawler = MyFeedCrawler(links, start_now=True)

    def signal_handler(signal, frame):
        crawler.stop()
    signal.signal(signal.SIGINT, signal_handler)

    crawler.start()