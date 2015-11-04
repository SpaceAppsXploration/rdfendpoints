"""
Utility class for semantic research in texts' bodies
"""

__author__ = 'lorenzo'

from unidecode import unidecode
from flankers.tagmeapi.tagMeService import TagMeService
from flankers.tools import retrieve_json


class TextSemantics(object):
    def __init__(self, text):
        self.text = unidecode(text)
        self.spotted = None
        self.get_spotted_terms()

    def find_related_concepts(self):
        """
        Find related concept in taxonomy from a text
        :return: a list of taxonomy keywords (see http://taxonomy.projectchronos.eu/concepts/c/infrared+telescopes)
        """
        #
        # Lookup terms in taxonomy and fetch relatedConcepts (keywords)
        # return related terms if they are found in the taxonomy

        return self.lookup_in_taxonomy()

    def find_related_missions(self, text):
        """
        Find and pass to the index missions related to arguments in a text
        :param text:
        :return:
        """
        pass

    def get_spotted_terms(self):
        """
        from spotted terms returns wikipedia slugs
        :param res: the JSON received from the Spotting API
        :return: a list of wikipedia slugs in an article
        """
        #
        # Find wikipedia terms in text
        # Spot terms in text
        #
        res = TagMeService.check_spotting(self.text)
        rst = []
        if res['spotted']:
            for s in [s['spot'] for s in res['value']['spots']]:
                r = TagMeService.retrieve_taggings(s.encode('utf-8'), method='POST')
                if len(r['annotations']) != 0:
                    for n in r['annotations']:
                        if 'title' in n.keys():
                            title = n['title'].replace(' ', '_')  # strip whitespaces from dbpedia tag
                            rst.append(title)
                            if len(rst) > 200:
                                # if the terms spotted are more than 199, enough
                                setattr(self, 'spotted', rst)
                                return None
                        else:
                            print "Cannot find title in annotations: " + str(n)

        setattr(self, 'spotted', rst)

    def lookup_in_taxonomy(self):
        """
        from wikipedia slugs fetch relatedConcepts in the taxonomy
        :param results: a list of wikipedia slugs
        :return: a set of related concepts to the slugs
        """
        from unidecode import unidecode

        base_url = "http://taxonomy.projectchronos.eu/space/dbpediadocs/{}"
        labels = []
        resource = None
        for res in self.spotted:
            res = unidecode(res)
            try:
                # print base_url.format(res)
                resource = retrieve_json(base_url.format(res))
            except Exception as e:
                print Exception('lookup_in_taxonomy(): Cannot fetch taxonomy: ' + res.encode('ascii', 'replace') + ' ' + str(e))

            if resource and 'relatedConcepts' in resource.keys():
                for c in resource['relatedConcepts']:
                    if c:
                        try:
                            resource = retrieve_json(c)
                        except Exception:
                            try:  # see bottom of the module
                                kwd = c[c.rfind('/') + 1:].replace("+", " ").strip()
                                # print kwd, kwd in to_be_corrected.keys()
                                taxonomy = "http://taxonomy.projectchronos.eu/concepts/c/{}"
                                if kwd in to_be_corrected.keys():
                                    kwd = to_be_corrected[kwd].replace(" ", "+")
                                    # print kwd
                                else:
                                    kwd = kwd.replace(" ", "+")
                                try:
                                    resource = retrieve_json(taxonomy.format(kwd))
                                except Exception as e:
                                    raise ValueError("Cannot deduce keyword. Cannot fetch relatedConcepts: " + str(e))
                            except ValueError as e:
                                print str(e)
                                continue
                            except Exception as e:
                                print Exception('lookup_in_taxonomy(): ' + c + ' Concept is not in the space api ' + str(e))
                                continue

                        # Resource is found in the taxonomy
                        label = resource['label']
                        labels.append(str(label))
        return set(labels)

    @classmethod
    def find_term_ancestorship(cls, term):
        """
        Return the genealogy of a term in the Taxonomy.

        :param term: a term in the taxonomy
        :return: a dictionary
        """
        term = term.replace(" ", "+").lower()
        print term
        base_url = "http://taxonomy.projectchronos.eu/concepts/c/{}"
        try:
            resource = retrieve_json(base_url.format(term))
        except Exception:
            raise ValueError("find_term_ancestorship(): term is not in the taxonomy. Wrong term.")

        def get_ancestor(obj, ancestors=tuple()):
            if 'ancestor' not in obj.keys():
                return ancestors

            new_obj = retrieve_json(obj['ancestor'])
            ancestors += (new_obj['label'], )
            return get_ancestor(new_obj, ancestors)

        return {
            "slug": term,
            "term": term.replace("+", " "),
            "ancestors": list(get_ancestor(resource))[::-1]
        }

#
# Workaround to avoid a bug in label sanitation in the Taxonomy server (commas)
# To be fixed when refactoring
#
to_be_corrected = {
    "acceleration effects (biological animal and plant)": "acceleration effects (biological, animal and plant)",
    "acceleration effects (biological human)": "acceleration effects (biological, human)",
    "altitude effects (biological animal and plant)": "altitude effects (biological, animal and plant)",
    "altitude effects (biological human)": "altitude effects (biological, human)",
    "atmospheric pressure effects (biological animal and plant)": "atmospheric pressure effects (biological, animal and plant)",
    "biographies of astronauts aviation pioneers pilots and": "biographies of astronauts, aviation pioneers, pilots, and",
    "electromagnetic devices (radiators sensors and other": "electromagnetic devices (radiators, sensors and other",
    "electromagnetic field effects (biological animal and plant)": "electromagnetic field effects (biological, animal and plant)",
    "electromagnetic field effects (physiological human)": "electromagnetic field effects (physiological, human)",
    "environmental effects (biological animal and plant)": "environmental effects (biological, animal and plant)",
    "fatigue (physiological human)": "fatigue (physiological, human)",
    "gravitational effects (biological animal and plant)": "gravitational effects (biological, animal and plant)",
    "gravitational effects (biological human)": "gravitational effects (biological, human)",
    "in-orbit maintenance servicing and refueling": "in-orbit maintenance, servicing and refueling",
    "isolation effects (psychological human)": "isolation effects (psychological, human)",
    "lighter-than-air craft (balloons airships) aerodynamics": "lighter-than-air craft (balloons, airships) aerodynamics",
    "lighter-than-air craft (balloons airships) design": "lighter-than-air craft (balloons, airships) design",
    "magnetic field effects (biological animal and plant)": "magnetic field effects (biological, animal and plant)",
    "magnets (electrical electronics application)": "magnets (electrical, electronics application)",
    "maintenance facilities (space based ground based)": "maintenance facilities (space based, ground based)",
    "microgravity effects (biological animal and plant)": "microgravity effects (biological, animal and plant)",
    "modulators (electric electronic devices)": "modulators (electric, electronic devices)",
    "optical scanners (computer peripheral equipment)": "optical scanners (computer, peripheral equipment)",
    "or are affected by design development testing": "or are affected by design, development, testing,",
    "passive sensors trackers and references (aircraft)": "passive sensors, trackers, and references (aircraft)",
    "passive sensors trackers and references (spacecraft)": "passive sensors, trackers, and references (spacecraft)",
    "perception (biological human)": "perception (biological, human)",
    "perception (psychological human)": "perception (psychological, human)",
    "propellant injectors pumps and tanks (spacecraft)" :"propellant injectors, pumps, and tanks (spacecraft)",
    "radiation effects (biological animal and plant)": "radiation effects (biological, animal and plant)",
    "propulsion effects on launching trajectories, and orbits": "propulsion effects on launching, trajectories, and orbits",
    "rail accelerators railguns launchers (applications)": "rail accelerators, railguns, launchers (applications)",
    "rail accelerators railguns launchers (theory)": "rail accelerators, railguns, launchers (theory)",
    "reduced gravity effects (biological animal and plant)": "reduced gravity effects (biological, animal and plant)",
    "reduced gravity effects (physiological human)": "reduced gravity effects (physiological, human)",
    "regulators (voltage current)": "regulators (voltage, current)",
    "repair facilities (space based ground based)": "repair facilities (space based, ground based)",
    "satellites for air land or sea navigation": "satellites for air, land or sea navigation",
    "satellites for air land or sea navigation control": "satellites for air, land, or sea traffic control",
    "sensory deprivation (physiological effects human)": "sensory deprivation (physiological effects, human)",
    "sensory deprivation (psychological effects human)": "sensory deprivation (psychological effects, human)",
    "sleep deprivation (physiological effects human)": "sleep deprivation (physiological effects, human)",
    "sleep deprivation (psychological effects human)": "sleep deprivation (psychological effects, human)",
    "sociological research (psychology human)": "sociological research (psychology, human)",
    "space adaptation (physiological human)": "space adaptation (physiological, human)",
    "space adaptation (psychological effects human)": "space adaptation (psychological effects, human)",
    "space environment effects (biological animal and plant)": "space environment effects (biological, animal and plant)",
    "space flight effects (physiological human)": "space flight effects (physiological, human)",
    "space flight effects (psychological human)": "space flight effects (psychological, human)",
    "special vehicles (land sea air)": "special vehicles (land, sea, air)",
    "stress (physiological effects human)": "stress (physiological effects, human)",
    "stress (psychological effects human)": "stress (psychological effects, human)",
    "stress effects of atmospheric flight (physiological human)": "stress effects of atmospheric flight (physiological, human)",
    "stress effects of space flight (physiological human)": "stress effects of space flight (physiological, human)",
    "temperature effects (biological animal and plant)": "temperature effects (biological, animal and plant)",
    "thin films (theory deposition and growth)": "thin films (theory, deposition and growth)",
    "weightlessness effects (biological animal and plant)": "weightlessness effects (biological, animal and plant)",
    "weightlessness effects (physiological human)": "weightlessness effects (physiological, human)",
    "weightlessness effects (psychological human)": "weightlessness effects (psychological, human)",
    "zero gravity effects (biological animal and plant) ": "zero gravity effects (biological, animal and plant)",
    "zero gravity effects (physiological human)": "zero gravity effects (physiological, human)"
}