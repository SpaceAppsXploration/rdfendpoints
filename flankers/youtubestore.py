import webapp2
import urllib

from apiclient.discovery import build
from optparse import OptionParser

from config.config import _DEBUG
from config.youtube_secret import _KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION
from datastore.models import WebResource


params = {
    'part': 'id, snippet',
    'q': 'space+exploration+documentary',
    'publishedAfter': '2005-01-01T00:00:00Z',
    'publishedBefore': '2005-01-01T00:00:00Z',
    'order': 'relevance'
}

### Advanced operators: https://support.google.com/youtube/answer/2685977?hl=en
# 'q': '##"some tag"' (double # operator)
# tags: space, science, space race, space exploration, astrophysics, astronomy, quantum physics


class YoutubeStore(webapp2.RequestHandler):
    """
    A very basic fetch and store for Youtube API
    """
    def get(self):
        def build_client():
            youtube = build(
                YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=_KEY
            )
            return youtube

        def fetch_data(client):
            data = client.search().list(
                q=params['q'],
                part=params['part'],
                maxResults=200,
                publishedAfter='2005-01-01T00:00:00Z'
            ).execute()

            return data

        def store_video(obj):
            WebResource.store_youtube_video(obj)

        def store_response(resp):
            for video in resp.items:
                store_video(video)

        client = build_client()
        response = fetch_data(client)
        store_response(response)

        # note: pageToken = response.nextPageToken
        return None

'''
{
   "kind": "youtube#searchResult",
   "etag": "\"oyKLwABI4napfYXnGO8jtXfIsfc/MK_9fr0vi4jxlpvMPSqUZ7cnXXE\"",
   "id": {
    "kind": "youtube#video",
    "videoId": "ZtaKWt26dNs"
   },
   "snippet": {
    "publishedAt": "2015-02-20T19:14:29.000Z",
    "channelId": "UCIR_LPmEQ9QHR0yB2lxgaxQ",
    "title": "Space Exploration - \"Our Universe\" (Episode 01) [2015 Documentary]",
    "description": "On this episode of Space Exploration - \"Our Universe\" [2015 Documentary], ongoing journey to discovery celestial structures in outer space.Extreme space ...",
    "thumbnails": {
     "default": {
      "url": "https://i.ytimg.com/vi/ZtaKWt26dNs/default.jpg"
     },
     "medium": {
      "url": "https://i.ytimg.com/vi/ZtaKWt26dNs/mqdefault.jpg"
     },
     "high": {
      "url": "https://i.ytimg.com/vi/ZtaKWt26dNs/hqdefault.jpg"
     }
    },
    "channelTitle": "NewerDocumentaries",
    "liveBroadcastContent": "none"
   }
  }
'''


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/storeyoutube', YoutubeStore),
], debug=_DEBUG)
