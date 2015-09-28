import json
from scripts.remote.remote import get_curling
from config.config import _CLIENT_TOKEN, _ENV, _SERVICE

__author__ = 'Lorenzo'


def download_ids_generator(results=(), bookmark='start', environment='offline'):
    """
    Recursive - Fetch and collect all the resources' ids in the datastore
    :param results: list of the collected ids
    :param bookmark: bookmark to fetch different datastore's pages
    :return: results list
    """
    import itertools

    to_append = get_curling(_ENV[environment]['_SERVICE'] + '/datastore/index',
                            {'token': _CLIENT_TOKEN,
                             'bookmark': bookmark if bookmark != 'start' else ''})
    to_append = json.loads(to_append)

    if not to_append['next']:
        return itertools.chain(results, iter(to_append['articles']))

    return download_ids_generator(
        results=itertools.chain(results, iter(to_append['articles'])),
        bookmark=to_append['next']
    )

'''
iterated = download_ids_generator(environment='offline')
for uuid in iterated:
    print uuid
    next(iterated)
'''

def dump_to_triple_store():
    """
    Dump chronos:webresource objects in the triple store
    :return:
    """
    from scripts.remote.remote import post_curling

    print "downloading ids... wait"
    ids = download_ids_generator()
    print "download finished"

    triples = str()
    for uuid in ids:
        subject = str('<' + _SERVICE + '/data/webresource/' + str(uuid) + '>')
        triple = subject
        triple += '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
        triple += '<http://ontology.projectchronos.eu/chronos/webresource> . '
        triples += triple
        try:
            next(ids)
        except StopIteration:
            break

    print triples
    post_curling('http://localhost:8080/sparql', {'token': _CLIENT_TOKEN, 'triple': triples}, display=True)

dump_to_triple_store()