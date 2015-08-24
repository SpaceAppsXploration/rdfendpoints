__author__ = ['niels', 'lorenzo']

import os

_GRAPH_ID = 'default-graph'
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

_TEMP_SECRET = "************"


def set_env_variables():
    if not 'SERVER_SOFTWARE' in os.environ or os.environ['SERVER_SOFTWARE'].startswith('Development'):
        _SERVICE = "http://localhost:8080"
        _REST_SERVICE = "http://localhost:8080/database/cots/"
        _COMPONENTS_URL = "http://localhost:8080/database/cots/store"
    else:
        _SERVICE = "http://rdfendpoints.appspot.com"
        _REST_SERVICE = "http://rdfendpoints.appspot.com/database/cots/"
        _COMPONENTS_URL = "http://rdfendpoints.appspot.com/database/cots/store"




    return _SERVICE, _REST_SERVICE, _COMPONENTS_URL

_SERVICE, _REST_SERVICE, _COMPONENTS_URL = set_env_variables()

_PATH = os.path.join(os.path.dirname(__file__), 'templates')
