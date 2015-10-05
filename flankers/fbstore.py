import webapp2
import urllib
import json

from config.config import _DEBUG
from config.fb_secret import fb_appid, fb_secret
from datastore.models import WebResource

__author__ = 'Lorenzo'


def generate_token():
    """
    Generate FB API token, needed to access the REST API
    :return: 'access_token=<token>'
    """
    url = 'https://graph.facebook.com/oauth/access_token'
    params = {
        'client_id': fb_appid,
        'client_secret': fb_secret,
        'grant_type': 'client_credentials'
    }
    url = url + '?' + urllib.urlencode(params)
    print url
    response = urllib.urlopen(url)
    return str(response.read())


token = generate_token()
aliases = ['GuntersSpacePage', 'SETIInstitute']


class FBStore(webapp2.RequestHandler):
    """
    A very basic fetch and store for FB posts
    """

    def get(self):
        try:
            [self.get_wall_posts(a) for a in aliases]
        except Exception as e:
            raise Exception('FBStore Handler - Error in get(): ' + str(e))

        self.response.status = 200
        return self.response.write('Done')

    def get_wall_posts(self, alias):
        url = 'https://graph.facebook.com/' + alias + '/posts?' + token

        def get_wall_recursive(url):
            response = urllib.urlopen(url)
            response = json.loads(response.read())
            if 'error' not in response.keys():
                for o in response['data']:
                    WebResource.store_fb_post(alias, o)
            else:
                from flankers.errors import RESTerror
                raise RESTerror('get_wall_recursive(): FB API error')

            if 'paging' not in response.keys() or not response['paging']['next']:
                return None

            return get_wall_recursive(response['paging']['next'])

        return get_wall_recursive(url)


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/storefb', FBStore),
], debug=_DEBUG)
