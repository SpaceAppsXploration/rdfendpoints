#
# A basic API to query TagMe RESTful services
#

__author__ = ['lorenzo@pramantha.net']


import requests
import time
from pprint import pprint
import urllib

from flankers.tagmeapi.secret.keys import return_api_key
from flankers.tools import retrieve_json

api_key = return_api_key()


class TagMeService:
    """
    Contains methods that format inputs and fetch the required data from the service
    --------------------------------------------------------------------------------
    """

    @staticmethod
    def return_gen_scopes():
        return ['Aerospace', 'Astrophysics', 'Cosmic_ray', 'Spaceflight', 'Spacecraft', 'Avionics', "Command_and_control",
                "Geodesy", 'Astronomical_object', 'Astronomy', 'Aircraft', 'Atmosphere',
                "Navigation", "Radio_navigation", "Satellite", "Spaceflight", "Physics",
                "NASA", "Planetary_science"]

    @staticmethod
    def check_spotting(text):
        """
        Spot wikipedia references in a given text
        'http://tagme.di.unipi.it/spot?key=****&text=Recent+poll+show+President+Obama+opening+up+a+small+lead'
        :param text: the text to analyze
        :return: dictionary with a flag message ('spotted') and a loaded JSON from response ('value')
        """
        import simplejson as json
        endpoint = "http://tagme.di.unipi.it/spot"

        body = str(text)


        params = {
            "key": api_key,
            "text": body
        }
        url = endpoint + '?' + urllib.urlencode(params)
        try:
            answer = json.loads(requests.get(url).text)
        except (Exception, UnicodeDecodeError):
            print(">>>>>>>>>>>>>>>>> ERROR >>>>>>>>>>", text)
            return {"spotted": False, "value": None}

        if len(answer["spots"]) != 0:
            result = {"spotted": True, "value": answer}
            return result

        return {"spotted": False, "value": answer}

    @staticmethod
    def retrieve_taggings(term, method='GET'):
        """
        Find annotations of a given concept/word/sets of words
        'http://tagme.di.unipi.it/tag?key=****&text=Recent+poll+show+President+Obama+opening+up+a+small+lead'
        :param term: the text to analyze as a byte (b'string')
        :return: dictionary with loaded JSON from response
        """
        endpoint = "http://tagme.di.unipi.it/tag"
        # print(term)
        if str(term) == 'None':
            return {"timestamp": time.time(), "time": 0, "api": "tag", "annotations": [], "lang": "en"}
        params = {
            "key": api_key,
            "text": term,
            "include_categories": True,
            "include_abstract": True,
            "include_all_spots": True
        }
        if method == 'GET':
            url = endpoint + '?' + urllib.urlencode(params)
            data = None
        # print(url)
        elif method == 'POST':
            url = endpoint
            data = params
        else:
            raise BadRequest('retrieve_taggings(): Wrong HTTP Verb')

        results = {"timestamp": time.time(), "time": 0, "api": "tag", "annotations": [], "lang": "en"}
        try:
            results = retrieve_json(url, method=method, data=data)
        except (Exception, ValueError):
            return results

        if "errors" not in results.keys() or results["errors"] == 0:
            return results

        raise BadRequest('retrieve_taggings() Failed')

    @classmethod
    def relate(cls, titles, comparing=None, min_rho=0.44):
        """
        Implement the TagMe's 'relating API'
        :param titles: a string that is wikipedia title or a list of titles
        :param comparing: a string that is wikipedia title or a list of titles
        :param min_rho: the minimum rho to filter the relation
        :return: a list of results objects with "rel" > min_rho
        """
        endpoint = "http://tagme.di.unipi.it/rel"
        if comparing is None:
            comparing = cls.return_gen_scopes()

        params = {
            "key": api_key,
            "tt": []
        }

        if isinstance(titles, list):
            if len(titles) > 1:
                if isinstance(comparing, list):
                    [params["tt"].append(t + ' ' + c) for c in comparing for t in titles if t != c]
                elif isinstance(comparing, str):
                    [params["tt"].append(t + ' ' + comparing) for t in titles if t != comparing]
            elif len(titles) == 1:
                if isinstance(comparing, list):
                    [params["tt"].append(titles[0] + ' ' + c) for c in comparing if titles[0] != c]
                elif isinstance(comparing, str):
                    params["tt"].append(titles[0] + ' ' + comparing)
            else:
                raise ConceptNotInDBpedia('This term does not have annotations, so it cannot be searched for related')
        else:
            if isinstance(comparing, list):
                [params["tt"].append(titles + ' ' + c) for c in comparing if titles != c]
            elif isinstance(comparing, str):
                params["tt"].append(titles + ' ' + comparing)

        url = endpoint + '?' + urlencode(params, True)

        try:
            results = retrieve_json(url)
            pprint(results)
        except (Exception, ValueError):
            raise BadRequest('Error in connection or in JSON parsing the response from TagMe Relating API')

        try:
            if int(results["errors"]) == 0 or len(results["result"]) == 0:
                output = [r for r in results["result"] if float(r["rel"]) > min_rho]
                return output
            else:
                for r in results["result"]:
                    if 'err' in r.keys():
                        print(BadRequest("Error in request data to TagMe: " + str(r['err'] + " in " + str(r))))
                        return None
        except (Exception, KeyError) as e:
            raise e

        raise BadRequest('TagMe API responded with an error: ' + str(results))


class ConceptNotInDBpedia(Exception):
    """
    terms passed to the API have no annotations from WikiPedia
    """
    pass


class BadRequest(Exception):
    """
    Request returned with some error
    """
    pass


class TextNotSpotted(Exception):
    """
    No terms where found in the string
    """
    pass


if __name__ == "__main__":
    print("This is a useful module, not a stand-alone script")