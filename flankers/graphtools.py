"""
Tools for SPARQL querying and other Graph utilities.

Try to collect here all the operations that involves Graph()
"""

__author__ = 'niels'

from rdflib import Graph

from datastore.ndbstore import NDBStore
from config.config import _VOC_GRAPH_ID, _WEBRES_GRAPH_ID, _CONCEPTS_GRAPH_ID


def graph(graph_id=_VOC_GRAPH_ID):
    """
    Return a Graph with a particular name
    :param graph_id: graph identification
    :return: a Graph() instance
    """
    return Graph(store=NDBStore(identifier=graph_id))


def update(q):
    graph().update(q)


def query(q):
    """
    Query a single Graph() instance (default graph)
    :param q:
    :return: JSON
    """
    response = graph().query(q)
    if response.type == 'CONSTRUCT': #These cannot be JSON-serialized so we extract the data with a SELECT
        g = Graph()
        g += response
        response = g.query("SELECT ?s ?p ?o WHERE {?s ?p ?o}")
    return response.serialize(format='json')


def query_all(q):
    """
    Query all the shard
    :return:

    http://rdflib.readthedocs.org/en/latest/apidocs/rdflib.html?highlight=graph%20name#rdflib.graph.ConjunctiveGraph
    >>> vocabgraph = Graph(store=NDBStore(identifier=graph_id))
    >>> combined_graph = rdflib.graph.ReadOnlyGraphAggregate([vocab_graph, concept_graph, crawled_graph])
    >>> for (p, o) in combined_graph.predicate_objects(my_uri_ref):
    >>>     do_stuff(p, o)
    """
    import rdflib
    vocabularies = Graph(store=NDBStore(identifier=_VOC_GRAPH_ID))
    webresources = Graph(store=NDBStore(identifier=_WEBRES_GRAPH_ID))
    concepts = Graph(store=NDBStore(identifier=_CONCEPTS_GRAPH_ID))
    combined_graph = rdflib.graph.ReadOnlyGraphAggregate([vocabularies, webresources, concepts])
    response = combined_graph.query(q)
    if response.type == 'CONSTRUCT': #These cannot be JSON-serialized so we extract the data with a SELECT
        g = Graph()
        g += response
        response = g.query("SELECT ?s ?p ?o WHERE {?s ?p ?o}")
    return response.serialize(format='json')


def store_triples(triples, graph_id=_VOC_GRAPH_ID, format="nt"):
    """
    Cache and store the new triples
    :param triples: triples POSTed
    :return: graphs
    """
    cache_graph = Graph()
    cache_graph.parse(data=triples, format=format)
    app_graph = graph(graph_id)
    app_graph += cache_graph
    return app_graph, cache_graph