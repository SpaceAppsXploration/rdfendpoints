__author__ = 'lorenzo'

from flankers.tagmeapi.tagMeService import TagMeService
from flankers.tools import retrieve_json


def find_related_concepts(text):
    """
    Find related concept in taxonomy from a text
    :param text: a given abstract or title
    :return: a list of taxonomy keywords (see http://taxonomy.projectchronos.eu/concepts/c/infrared+telescopes)
    """
    #
    # Find wikipedia terms in text
    # Spot terms in text
    text = text.encode('ascii', 'replace')
    response = TagMeService.check_spotting(text)

    results = return_wikipedia_term(response)

    #
    # Lookup terms in taxonomy and fetch relatedConcepts (keywords)
    # return related terms if they are found in the taxonomy

    return lookup_in_taxonomy(results)


def return_wikipedia_term(res):
    """
    from spotted terms returns wikipedia slugs
    :param res: the JSON received from the Spotting API
    :return: a list of wikipedia slugs in an article
    """
    rst = []
    if res['spotted']:
        for s in [s['spot'] for s in res['value']['spots']]:
            r = TagMeService.retrieve_taggings(s.encode('utf-8'), method='POST')
            if len(r) != 0:
                for n in r['annotations']:
                    title = n['title'].replace(' ', '_')  # strip whitespaces from dbpedia tag
                    rst.append(title)
    return rst


def lookup_in_taxonomy(results):
    """
    from wikipedia slugs fetch relatedConcepts in the taxonomy
    :param results: a list of wikipedia slugs
    :return: a set of related concepts to the slugs
    """
    base_url = "http://taxonomy.projectchronos.eu/space/dbpediadocs/{}"
    labels = []
    resource = None
    for res in results:
        try:
            # print base_url.format(res)
            resource = retrieve_json(base_url.format(res))
        except Exception as e:
            print Exception('Cannot fetch taxonomy: ' + res + ' ' + str(e))

        if resource and 'relatedConcepts' in resource.keys():
            for c in resource['relatedConcepts']:
                if c:
                    label = c[c.rfind('/') + 1:].replace('+', ' ')
                    # print 'Found! ' + label
                    labels.append(str(label))
    return set(labels)
