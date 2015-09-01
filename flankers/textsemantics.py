__author__ = 'lorenzo'

from flankers.tagmeapi.tagMeService import TagMeService
from flankers.tools import retrieve_json


def find_related_concepts(text):
    """
    Find related concept in taxonomy from a text
    :param text: a given abstract or title
    :return: a list of taxonomy keywords (see http://taxonomy.projectchronos.eu/concepts/c/infrared+telescopes)
    """
    # TagMeService.spot
    # TagMeService.tag
    # lookup tags in taxonomy.projectchronos.eu
    # if lookup:
    #    fetch(url) > relatedConcepts
    # for relatedConcepts:
    #    fetch(url) > label
    # return [labels]

    #
    # Find wikipedia terms in text
    #
    results = TagMeService.check_spotting(text)
    if results['spotted']:
        results = []
        for spot in [s['spot'] for s in TagMeService.check_spotting(text)['value']['spots']]:
            result = TagMeService.retrieve_taggings(spot.encode('utf-8'), method='POST')
            for n in result['annotations']:
                title = n['title'].replace(' ', '_')  # strip whitespaces from dbpedia tag
                results.append(title)

    #
    # Lookup terms in taxonomy and fetch relatedConcepts (keywords)
    #

    base_url = "http://taxonomy.projectchronos.eu/space/dbpediadocs/{}"
    labels = []
    resource = None
    for res in results:
        try:
            # print base_url.format(res)
            resource = retrieve_json(base_url.format(res))
        except Exception as e:
            print Exception('Cannot fetch taxonomy: ' + res + ' ' + str(e))

        if 'relatedConcepts' in resource.keys() and resource:
            for c in resource['relatedConcepts']:
                if c:
                    label = c[c.rfind('/') + 1:].replace('+', ' ')
                    # print 'Found! ' + label
                    labels.append(str(label))
    return set(labels)


