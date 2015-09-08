import webapp2
from config.config import _TEMP_SECRET

__author__ = 'Lorenzo'


class Crawling(webapp2.RequestHandler):
    """
    /database/crawling/store POST: Service handler for operations on crawled resources
    """
    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        if self.request.get('pwd') == _TEMP_SECRET and self.request.get('resource'):
            from datastore.models import WebResource
            try:
                oid = WebResource.dump_from_json(self.request.get('resource'))
            except (Exception, ValueError) as e:
                self.response.status = 400
                return self.response.write('The request could not be understood, wrong resource format or syntax: ' + str(e))
            self.response.status = 200
            return self.response.write('Resource Stored: ' + str(oid))
        else:
            self.response.status = 405
            return self.response.write('Not Authorized')


class FourOhFour(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(404)


class Testing(webapp2.RequestHandler):
    """
    /test: test handler
    """
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        try:
            from bs4 import BeautifulSoup
            from json2html import __version__
        except Exception as e:
            raise e
        self.response.write('test passed')