"""
Main Script for generating and converting JSON to JSON-LD about components for subsystems
(to be dumped and uploaded as triples)
"""

__author__ = 'lorenzo'

import sys
import json
from remote import post_curling
from config.config import _TEMP_SECRET, _COMPONENTS_URL


from scripts.datagenerator.constraints import tech_constrains
from scripts.factory import SubSystem


def generate_metaclasses():
    """
    NOTED FUNCTION - not implemented
    :return:
    """
    classes = {}
    for k, v in tech_constrains.items():
        # doc for type > https://docs.python.org/2/library/functions.html#type
        # usage http://stackoverflow.com/a/15247202/2536357
        classname = "%s" % SubSystem.stringify(k)
        print classname
        classes[classname] = (type(classname, (SubSystem,), v))
    return classes


def _upload_subsystems(n, url=_COMPONENTS_URL):
    """
    upload to server the subsystems instances
    NOTE: dumped via a REST endpoint /database that has not been created yet
    endpoint: POST /database/cots/store {"pwd": ***, "data": {...} }
    :param url: the server endpoint
    :param n: number of iteration per family to be generated
    :return:
    """
    try:
        int(n)
    except ValueError:
        raise ValueError('Argument must be an integer')

    for i in range(0, int(n)):
        # generate py instance components and translate in JSON-LD format
        instances = [SubSystem.generate_py_instance(k, v) for k, v in tech_constrains.items()]
        jsonlds = [SubSystem.generate_jsonld(c) for c in instances]

        for j in jsonlds:
            # upload to datastore (under construction)
            post_curling(url=url,
                         params={'pwd': _TEMP_SECRET, 'data': json.dumps(j)},
                         display=True)


if __name__ == "__main__":
    try:
        _upload_subsystems(sys.argv[1], sys.argv[2])
    except IndexError:
        _upload_subsystems(sys.argv[1])

