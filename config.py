__author__ = 'lorenzo'

import os

_GRAPH_ID = 'default-graph'
_GRAPH_INSTANCE_ID = 'Graph-instance'

_VOCS = {
    'astronomy': 'http://ontology.projectchronos.eu/astronomy',
    'solarsystem': 'http://ontology.projectchronos.eu/solarsystem',
    'engineering': 'http://ontology.projectchronos.eu/engineering',
    'subsystems': 'http://ontology.projectchronos.eu/subsystems',
    'spacecraft': 'http://ontology.projectchronos.eu/spacecraft',
    'sensors': 'http://ontology.projectchronos.eu/sensors'
}

_TEMP_SECRET = '***'

_SERVICE = 'http://rdfendpoints.appspot.com/ds'

_PATH = os.path.join(os.path.dirname(__file__), 'templates')
