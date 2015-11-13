import webapp2
import json
import logging

from google.appengine.ext.webapp import template

from flankers.graphtools import query
from config.config import _DEBUG
from datastore.models import N3Cache


__author__ = 'Lorenzo'


map = {
    'planets': 'SELECT * WHERE { ?bodies <http://www.w3.org/1999/02/22-rdf-syntax-ns#type><http://ontology.projectchronos.eu/astronomy/Planet> . }',
    'sun': 'SELECT * WHERE { ?bodies <http://ontology.projectchronos.eu/astronomy/orbiting><http://ontology.projectchronos.eu/solarsystem/Sun>. }',
    'all_sats': 'SELECT * WHERE { ?bodies <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontology.projectchronos.eu/astronomy/Natural_satellite> . }'
}


def get_link(url):
    """
    Get the dbpedia url from a chronos ontology url by fetching the entity and checking the rdf:sameAs property
    :param url: a ontology.projectchronos.eu entity
    :return: str, the url of the dbpedia resource
    """
    from scripts.remote.remote import google_urlfetch

    rdf = google_urlfetch(url, {'format': 'jsonld'})
    rdf = json.loads(rdf)
    sameas = rdf['owl:sameAs']
    return sameas


def dbpedia_url(obj):
    if isinstance(obj, list):
        o = obj.pop()
        return str(o['@id']) if o['@id'].find('dbpedia') != -1 else dbpedia_url(obj)
    else:
        raise ValueError('flankers.extCaching.dbpediaurl: input must be a list')


class N3Caching(webapp2.RequestHandler):
    """
    A very basic cache for Ntriples strings
    #TO-DO: implement long-task
    """

    def get(self):
        """
        Handler for the cronjob: /cron/n3caching
        It stores XML data from external sources
        """
        from google.appengine.api import urlfetch
        logging.getLogger().handlers[0].setLevel(logging.DEBUG)

        for k, v in map.items():
            results = query(v)  # run the SPARQL query

            results = json.loads(results)
            urls = [r['bodies']['value'] for r in results['results']['bindings']]

            for u in urls:
                l = dbpedia_url(get_link(u))
                if l.endswith('.ntriples'):
                    l = l[:-9]
                print l
                try:
                    response = urlfetch.fetch(l)
                    if response.content.startswith('<?xml version="1.0"'):
                        try:
                            n3 = N3Cache(id=l, n3=response.content)
                            print "Storing resource"
                            n3.put()
                        except Exception:
                            print "Error or already stored"
                            pass
                    else:
                        print "ERROR: NO XML: " + str(response)
                except Exception as e:
                    print e



application = webapp2.WSGIApplication([
    webapp2.Route('/cron/n3caching', N3Caching),
], debug=_DEBUG)

