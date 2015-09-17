from urlparse import urlparse
import json
import logging

import webapp2
from google.appengine.ext import ndb

from scripts.remote.remote import dump_to_ds_post

__author__ = 'Lorenzo'

webresource_prop_map = {
    'url': {
        'prop': 'http://schema.org/url',
        'type': 'https://schema.org/URL'
    },
    'title': {
        'prop': 'http://schema.org/headline',
        'type': 'https://schema.org/Text'
    },
    'abstract': {
        'prop': 'https://schema.org/about',
        'type': 'https://schema.org/Text'
    },
    'published': {
        'prop': 'http://schema.org/datePublished',
        'type': 'https://schema.org/DateTime'
    },
}


class PublishWebResources(webapp2.RequestHandler):
    """
    GET data/webresource/<key>
    Serve datastore model WebResource as a NTRIPLES, for the purpose of the cloud:

    Linked Data to be served (JSON-LD format):
        {
          "@id": "http://hypermedia.projectchronos.eu/data/webresource/<key>",
          "@type": [
              "http://ontology.projectchronos.eu/chronos/webresource",
              "https://schema.org/Article"
          ]
        }

    :return Ntriple string
    """
    def get(self, key):
        from datastore.models import WebResource

        try:
            key = ndb.Key(urlsafe=key)
            obj = key.get()
        except Exception:
            key = ndb.Key(WebResource, int(key))
            obj = key.get()
        except:
            raise TypeError('Wrong Format of NDB key')

        url = str(obj.url)
        author = urlparse(url).netloc
        if url.find('twitter.com') != -1 and len(str(obj.abstract)) != 0:
            # obj is a tweet
            schema_type = 'https://schema.org/SocialMediaPosting'
        elif url.find('twitter.com') != -1 and len(str(obj.abstract)) == 0:
            # obj is link or media
            schema_type = 'https://schema.org/MediaObject'
        else:
            # obj is an article
            schema_type = 'https://schema.org/Article'

        result = {
            "@id": "http://hypermedia.projectchronos.eu/data/webresource/" + key.urlsafe(),
            "@type": schema_type,
            "https://schema.org/author": {
                '@value': author,
                '@type': 'https://schema.org/Text'
            }
        }
        for k, v in webresource_prop_map.items():
            result[v['prop']] = {
                '@value': obj.dump_to_json()[k],
                '@type': v['type']
            }

        #
        # Custom translation to ntriples (to be better designed)
        #
        results = str()
        for k in result.keys():
            if k != '@id':
                results += '<' + result['@id'] + '>' # add subject
                if isinstance(result[k], str):
                    results += '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' # predicate
                    results += '<' + result[k] + '> . ' # add object
                else:
                    if result[k]['@value']:
                        results += '<' + k + '>' # add predicate
                        results += '<' + result[k]['@value'] + '> . ' # add object'''

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = "application/n-triples; charset=utf-8"
        return self.response.out.write(
            results
        )


class PublishConcepts(webapp2.RequestHandler):
    """
    Serve taxonomy entity as a NTRIPLES, for the purpose of the cloud:

        Fetch from taxonomy:
            {
                "label": "infrared telescopes",
                "url": "http://taxonomy.projectchronos.eu/concepts/c/infrared+telescopes#concept",
                "group": "keywords",
                "ancestor": "http://taxonomy.projectchronos.eu/concepts/c/astronomy#concept"
            }

        Linked Data shape of the data:
            {
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#label": "infrared telescopes",
                "@type": "http://ontology.projectchronos.eu/chronos/concept"
                "@id": "http://hypermedia.projectchronos.eu/data/concept/infrared+telescopes",
                "http://ontology.projectchronos.eu/chronos/group": {
                    "@id": "http://ontology.projectchronos.eu/chronos/keyword"
                }
                "http://ontology.projectchronos.eu/chronos/relAncestor": {
                    "@id": "http://taxonomy.projectchronos.eu/concepts/c/astronomy#concept"
                }
            }
    :param label: it's a slugified version of the concept label (i.e. 'infrared+telescopes')
    :return Ntriple string
    """
    def get(self, label):
        from google.appengine.api import urlfetch

        base_url = 'http://taxonomy.projectchronos.eu/concepts/c/'
        url = base_url + label

        response = urlfetch.fetch(url)

        content = response.content
        status = response.status_code

        if status == 200:
            results = str()
            result = json.loads(content)
            if result['group'] == 'keywords':
                # add type
                _id = str('<http://hypermedia.projectchronos.eu/data/concept/' + label + '>')
                results += _id  # add subject
                results += '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'  # predicate
                results += '<http://ontology.projectchronos.eu/chronos/concept> .'  # add object
                for k in result.keys():
                    results += '<http://hypermedia.projectchronos.eu/data/concept/' + label + '>' # add subject
                    if k == 'label':
                        results += '<http://www.w3.org/1999/02/22-rdf-syntax-ns#label>' # predicate
                        results += '<' + result['label'] + '> . ' # add object
                    elif k == 'ancestor':
                        results += 'http://ontology.projectchronos.eu/chronos/relAncestor' # predicate
                        results += '<' + result['ancestor'] + '> . ' # add object
                    elif k == 'group':
                        results += '<http://ontology.projectchronos.eu/chronos/group>' # predicate
                        results += '<http://ontology.projectchronos.eu/chronos/keyword> . ' # add object'''

                self.response.headers['Access-Control-Allow-Origin'] = '*'
                self.response.headers['Content-Type'] = "application/n-triples; charset=utf-8"
                return self.response.write(results)
            else:
                raise Exception("Label is in the taxonomy but it's not a keyword")

        else:
            raise Exception("Wrong Label or Server Not Reachable")





