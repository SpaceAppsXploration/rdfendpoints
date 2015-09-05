import webapp2
import json
from datastore.models import Component
from config.config import _TEMP_SECRET, _HYDRA_VOCAB
from flankers.errors import format_message

__author__ = 'Lorenzo'



class Endpoints(webapp2.RequestHandler):
    """
    /database/cots/ GET: Serves (HATEOAS) JSON objects from the datastore, mostly COTS components
    /database/cots/store POST: store component instance in the datastore
    """
    def get(self, keywd):
        from flankers.tools import valid_uuid, families

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'
        if not keywd:
            # keywd is None serves the entrypoint view
            from config.config import _VOCS, _REST_SERVICE
            self.response.headers['Access-Control-Expose-Headers'] = 'Link'
            self.response.headers['Link'] = '<' + _HYDRA_VOCAB + '>;rel="http://www.w3.org/ns/hydra/core#apiDocumentation'
            results = [{"name": f[f.rfind('_') + 1:],
                        "collection_ld+json_description": _VOCS['subsystems'] + f + '/' + '?format=jsonld',
                        "collection_n-triples_description": _VOCS['subsystems'] + f,
                        "go_to_collection": _REST_SERVICE + f}
                       for f in families]
            return self.response.write(json.dumps(results, indent=2))
        elif keywd == 'ntriples' and self.request.get('uuid'):
            # url is "url/cots/ntriples?key=<uuid>"
            uuid = self.request.get('uuid')
            if valid_uuid(uuid):
                # return ntriples of the object
                return self.response.write(format_message("N-Triples not yet implemented"))
        elif valid_uuid(keywd):
            # if the url parameter is an hex, this should be a uuid
            # print a single component (in JSON with a link to N-Triples)
            if self.request.get('format') and self.request.get('format') == 'jsonld':
                # if user asks for JSON-LD
                self.response.headers['Content-Type'] = 'application/ld+json'
                try:
                    body = Component.parse_to_jsonld(keywd)
                except ValueError as e:
                    return self.response.write(format_message(e))
                return self.response.write(body)
            else:
                # serve JSON
                try:
                    body = Component.parse_to_json(keywd)
                except ValueError as e:
                    return self.response.write(format_message(e))
                return self.response.write(body)

        elif keywd in families:
            # if the url parameter is a family name
            # print the list of all the components in that family
            results = Component.restify(Component.get_by_collection(keywd))
            return self.response.write(results)
        else:
            # wrong url parameters
            return self.response.write(format_message("Not a valid key/id in URL"))

    def post(self, keywd):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        if keywd == 'store' and self.request.get('pwd') == _TEMP_SECRET:
            jsonld = self.request.get('data')
            from datastore.models import Component
            key = Component.dump_from_jsonld(jsonld)
            return self.response.write("COMPONENT STORED OK: {}".format(key))
        else:
            self.response.status = 405
            return self.response.write('Not Authorized')
