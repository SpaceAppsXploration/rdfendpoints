__author__ = ['niels', 'lorenzo']

import os

global socket

_VOC_GRAPH_ID = 'vocabularies-graph'
_WEBRES_GRAPH_ID = 'webresources-graph'
_CONCEPTS_GRAPH_ID = 'concepts-graph'
_GRAPH_INSTANCE_ID = 'Graph-instance'

_VOCS = {
    'astronomy': 'http://ontology.projectchronos.eu/astronomy/',
    'solarsystem': 'http://ontology.projectchronos.eu/solarsystem/',
    'engineering': 'http://ontology.projectchronos.eu/engineering/',
    'subsystems': 'http://ontology.projectchronos.eu/subsystems/',
    'spacecraft': 'http://ontology.projectchronos.eu/spacecraft/',
    'sensors': 'http://ontology.projectchronos.eu/sensors/',
    'exploration': 'http://ontology.projectchronos.eu/exploration/'
}


_CLIENT_TOKEN = "******"

_ENV = {'offline': {'_SERVICE': 'http://localhost:8080',
                    '_DEBUG': True},
        'online': {'_SERVICE': 'http://hypermedia.projectchronos.eu',
                   '_DEBUG': True}}


def set_env_variables():
    if not 'SERVER_SOFTWARE' in os.environ or os.environ['SERVER_SOFTWARE'].startswith('Development'):
        _SERVICE, _DEBUG = _ENV['offline']['_SERVICE'], _ENV['offline']['_DEBUG']

    else:
        _SERVICE, _DEBUG = _ENV['online']['_SERVICE'], _ENV['online']['_DEBUG']

    _REST_SERVICE = _SERVICE + "/database/cots/"
    _COMPONENTS_URL = _SERVICE + "/database/cots/store"
    _HYDRA_VOCAB = _SERVICE + "/hydra/vocab"

    return _SERVICE, _REST_SERVICE, _COMPONENTS_URL, _HYDRA_VOCAB, _DEBUG

_SERVICE, _REST_SERVICE, _COMPONENTS_URL, _HYDRA_VOCAB, _DEBUG = set_env_variables()


def articles_api_version(ver, endpoint='ALL'):
    if endpoint in _ARTICLES_API.keys():
        return _ARTICLES_API[endpoint][ver]

_ARTICLES_API = {
    "ALL": {
        "03": _SERVICE + "/articles/?api=true&",
        "04": _SERVICE + "/articles/v04/"
    },
    "TYPE_OF": {
        "04": _SERVICE + "/articles/v04/article"
    }
}

_CRAWLING_POST = {'local': 'http://localhost:8080/database/crawling/store',
                  'remote': 'http://hypermedia.projectchronos.eu/database/crawling/store'}

_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

_XPREADER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'xpreader-client')

# Given slug for different query types
_MEMCACHE_SLUGS = {
    'ALL': 'WebResource_all',
    'TYPE_OF': 'Articles_type_of',
    'KEYWORDS': 'Keywords_for_',
    'KWD_BY_ARTICLE': 'Keywords_'
}