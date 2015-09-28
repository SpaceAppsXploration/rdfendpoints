import json
from scripts.remote.remote import get_curling
from config.config import _CLIENT_TOKEN, _ENV

__author__ = 'Lorenzo'


def download_ids(results=list(), bookmark='start', environment='offline'):
    """
    Recursive - Fetch and collect all the resources' ids in the datastore
    :param results: list of the collected ids
    :param bookmark: bookmark to fetch different datastore's pages
    :return: results list
    """
    to_append = get_curling(_ENV[environment]['_SERVICE'] + '/datastore/index',
                            {'token': _CLIENT_TOKEN,
                             'bookmark': bookmark if bookmark != 'start' else ''})
    to_append = json.loads(to_append)
    if not to_append['next'] or len(results) == 150:
        results += to_append['articles']
        return results

    results += to_append['articles']
    return download_ids(results, to_append['next'])

print(download_ids(environment='online'))

def dump_to_triple_store():
    """
    Dump chronos:webresource object in the triple store
    :return:
    """

    post_curling(url, {'pwd': _TEMP_SECRET, 'triple': triples.read()}, display=True)